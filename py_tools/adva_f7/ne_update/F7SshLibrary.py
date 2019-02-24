#! /usr/bin/env python
# _*_ coding: utf-8 *_*
'''
This is a library for ssh connection using pexpect
basing on TCClientLibrary
author: David Deng ddengca@gmail.com
'''

import time
import re
import os.path
# import string

import pexpect
from pexpect.pxssh import pxssh
# from pexpect.pxssh import ExceptionPxssh

from robot.api import logger
from HardwareIdFile import HardwareIdFile
from aid_convert import AID2SELECTOR_BY_MODTYPE

USE_PRINT = False

REGEX_FLAGS = re.MULTILINE | re.DOTALL

# PROMPT_PATTERN = r"([^ \n\r]+ ?> ?)$"
PROMPT_PATTERN = r"([^ \n\r]+@FSP3000C)>"
MAX_CONNECTIONS = \
    "Max. number of connections \([0-9]+\) to card [0-9]+-[0-9]+ reached."
READ_TIMEOUT = 5

DATA_TYPES_INT = ["DT_BYTE", "DT_WORD", "DT_DWORD", "DT_QWORD"]


def remove_non_printable(buffer):
    buffer = re.sub(
        r"\x1b(E | [^m]*m)", "", buffer)   # remove ASCII escape codes
    return buffer


def log_use_print(enable_print):
    global USE_PRINT
    USE_PRINT = enable_print


def log_info(msg):
    if USE_PRINT:
        print("INFO: " + msg)
    else:
        logger.info(msg)


def log_debug(msg):
    if USE_PRINT:
        print("DEBUG: " + msg)
    else:
        logger.debug(msg)


class F7SshSession(pxssh):

    def __init__(
            self, ipaddress, username="root", password="CHGME.1", **kwargs):
        pxssh.__init__(self)

        self.timeout = READ_TIMEOUT

        self.PROMPT = '# '

        if "sync_multiplier" in kwargs:
            kwargs["sync_multiplier"] = float(kwargs["sync_multiplier"])
        else:
            kwargs["sync_multiplier"] = 4.0

        self.login(
            ipaddress, username, password, auto_prompt_reset=False, **kwargs)
        self.read_until_prompt()
        '''
        self.PROMPT = r'[^\r\n]+> '
        self.sendline("tc-client -s%s -n%s\n" % (shelf, slot))
        i = self.expect(
            [pexpect.TIMEOUT, MAX_CONNECTIONS, self.PROMPT],
            timeout=self.timeout)
        if i == 0:
            raise RuntimeError("tc-client command timed out")
        elif i == 1:
            raise RuntimeError(self.match.group(0))

        log_debug("prompt_synced? %s" % self.sync_original_prompt())

        self.sendline()
        log_debug("prompt = '%s'" % self.try_read_prompt(1.0).lstrip())

        self.write("\n")
        self.read_until_prompt()
        '''

    def enter_configure_mode(self):
        # self.PROMPT = r'[^\r\n]@FSP3000C# '
        self.PROMPT = '[node 1]\r\nadmin@FSP3000C#'
        self.sendline("configure")
        self.read_until_prompt()

    def exit_configure_mode(self):
        self.PROMPT = r'[^\r\n]@FSP3000C>'
        self.sendline("exit")
        self.read_until_prompt()

    def __del__(self):
        self.logout()
        self.close()

    def write(self, cmd):
        self.read()
        if cmd[-1] not in ['\n', '\r']:
            self.sendline(cmd)
        else:
            self.send(cmd)

    def read(self):
        try:
            return pxssh.read_nonblocking(self, size=9999, timeout=0.5)
        except pexpect.TIMEOUT:
            return ""

    def read_until_prompt(self, timeout=READ_TIMEOUT):
        self.prompt()
        return self.before


class F7SshLibrary(object):
    """
    Class to handle TC CLIENT information.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, hwid_path=None):
        self.sessions = {}
        self.aid_dicts = {}

        self.hwfile = None
        if str(hwid_path) != "None":
            self.hwfile = HardwareIdFile(hwid_path)
        else:
            # Try to use default hardware_id.h file
            # in TCClientLibrary directory
            mod_path = os.path.join(os.path.dirname(__file__), "hardware_id.h")
            if os.path.isfile(mod_path):
                self.hwfile = HardwareIdFile(mod_path)

    def open_connection(
            self, alias, ipaddress, username="admin", password="CHGME.1a",
            module_type=None, **kwargs):
        """
        Opens connection via tc-client to a module.
        """
        self.sessions[alias] = F7SshSession(
            ipaddress, username, password, **kwargs)

        self.aid_dicts[alias] = {}
        if module_type and module_type in AID2SELECTOR_BY_MODTYPE:
            aid_dict = self.aid_dicts[alias]
            aid_dict.update(AID2SELECTOR_BY_MODTYPE[module_type])
            # for old_key in aid_dict.keys():
            #     new_key = old_key.replace("<s>", shelf).replace("<n>", slot)
            #     aid_dict[new_key] = aid_dict.pop(old_key)

    def close_connection(self, alias):
        """
        Closes connection via tc-client to a module.
        """
        self.sessions[alias].write("\x03")
        del self.sessions[alias]

    def _cleanup_buffer(self, buffer, cmd=None):
        if cmd:
            buffer = re.sub(re.escape(cmd), "", buffer)  # remove leading echo
        buffer = remove_non_printable(buffer)
        return buffer.strip()

    def set_read_timeout(self, alias, timeout):
        self.sessions[alias].timeout_read = timeout

    def write(self, alias, cmd):
        self.sessions[alias].write(cmd)

    def read(self, alias):
        buffer = self.sessions[alias].read()
        return self._cleanup_buffer(buffer)

    def read_until_prompt(self, alias, cmd=None):
        session = self.sessions[alias]
        buffer = session.read_until_prompt()
        return self._cleanup_buffer(buffer, cmd)

    def execute_command(self, alias, cmd, search_pattern=None):
        session = self.sessions[alias]
        session.read()
        session.write(cmd)
        response = self.read_until_prompt(alias, cmd)
        if search_pattern:
            match = re.search(search_pattern, response)
            if not match:
                raise RuntimeError(
                    "Could not find pattern '%s' in response:\n%s"
                    % (search_pattern, response))
            groups = match.groups()
            if groups:
                if len(groups) > 1:
                    return list(groups)
                else:
                    return groups[0]
            else:
                return match.group(0)
        else:
            return response

    def write_and_read_response(self, alias, cmd):
        logger.warn("DEPRECATED: Write And Read Response")
        return self.execute_command(alias, cmd)

    def _convert_did_to_hex_string(self, did):
        if isinstance(did, basestring):
            if did.startswith("0x"):
                did_str = did
            else:
                did_str = "0x" + did
        else:
            did_str = "0x%08X" % did
        return did_str

    def _datatype_is_int(self, data_type):
        return len(
            set(DATA_TYPES_INT).intersection(set(data_type.split('|')))) > 0

    def _convert_int_value_to_hex_bytes(self, data_type, value):
        if "DT_BYTE" in data_type:
            nbits = 8
        elif "DT_WORD" in data_type:
            nbits = 16
        elif "DT_DWORD" in data_type:
            nbits = 32
        elif "DT_QWORD" in data_type:
            nbits = 64
        else:
            raise ValueError("Invalid int data_type %s" % data_type)

        # handle hex strings, integer strings, or integers
        if isinstance(value, basestring) and value.startswith("0x"):
            value = int(value, 16)
        else:
            value = int(value)

        hex_string = hex((value + (1 << nbits)) % (1 << nbits))
        bytes = re.findall(r'.{1,2}', hex_string[2:].upper(), re.DOTALL)
        for i in range(len(bytes)):
            bytes[i] = "0x" + bytes[i]
        return bytes

    def get_data(self, alias, did):
        did_str = self._convert_did_to_hex_string(did)
        resp = self.execute_command(alias, "getdata 0 %s" % did_str)

        if "Value is INVALID" in resp:
            logger.warn("Value for DID %s is INVALID" % did_str)
            resp = re.sub(".*Value is INVALID.*", '', resp)

        resp = re.sub("[\r\n ]+", ' ', resp.strip(), flags=REGEX_FLAGS)
        bytes = resp.strip().split(' ')
        return bytes

    def get_idx_data(self, alias, did, idx):
        did_str = self._convert_did_to_hex_string(did)
        idx_str = self._convert_did_to_hex_string(idx)
        resp = self.execute_command(
            alias, "getidxdata 0 %s %s" % (did_str, idx_str))

        if "Value is INVALID" in resp:
            logger.warn("Value for DID %s is INVALID" % did_str)
            resp = re.sub(".*Value is INVALID.*", '', resp)

        resp = re.sub("[\r\n ]+", ' ', resp.strip(), flags=REGEX_FLAGS)
        bytes = resp.strip().split(' ')
        return bytes

    def set_data(self, alias, did, *bytes):
        did_str = self._convert_did_to_hex_string(did)
        val_str = ""
        for byte in bytes:
            if not isinstance(byte, basestring):
                if int(byte) > 255:
                    ValueError(byte)
                byte = "0x%02X" % byte
            val_str += byte + " "
        val_str = val_str.strip()

        session = self.sessions[alias]
        session.write("setdata 0 %s %s" % (did_str, val_str))
        time.sleep(1)
        session.read_until_prompt()

    def get_data_hex(self, alias, did):
        bytes = self.get_data(alias, did)
        data_hex = "0x" + ''.join(bytes)
        return data_hex

    def set_data_hex(self, alias, did, data_hex):
        if not isinstance(data_hex, basestring):
            data_hex = "%X" % data_hex
        elif data_hex.startswith("0x"):
            data_hex = data_hex[2:]
        bytes = re.findall(r'.{1,2}', data_hex, re.DOTALL)
        for i in range(len(bytes)):
            bytes[i] = "0x" + bytes[i]
        self.set_data(alias, did, *bytes)

    def get_data_formatted(self, alias, did, idx=0):
        if not self.hwfile:
            raise RuntimeError("No hardware ID file")

        if idx == 0:
            bytes = self.get_data(alias, did)
        else:
            bytes = self.get_idx_data(alias, did, idx)

        data_type = self.hwfile.get_datatype_by_did(did)

        # If integer, convert to either signed or unsigned
        if self._datatype_is_int(data_type):
            data_int = int(''.join(bytes), 16)
            if "DT_SIGNED" in data_type:
                if data_int > 0x7FFFFFFF:
                    data_int -= 0x100000000
            data_str = str(data_int)
        # If chunk, convert to hex string or null-terminated string
        elif "DT_CHUNK" in data_type:
            data_str = ""
            for byte in bytes:
                # DT_CHUNK|DT_SIGNED = null-terminated string
                if ("DT_SIGNED" in data_type) and (byte == "00"):
                    break
                data_str += chr(int(byte, 16))
        # If threshold, convert to single byte alarm value
        elif "DT_THRESHOLD" in data_type:
            if int(bytes[1], 16) & 0x20:
                data_str = "1"
            else:
                data_str = "0"
        else:
            raise ValueError("Unkown data_type %s" % data_type)

        return data_str

    def set_data_formatted(self, alias, did, value):
        if not self.hwfile:
            raise RuntimeError("No hardware ID file")

        data_type = self.hwfile.get_datatype_by_did(did)

        if self._datatype_is_int(data_type):
            bytes = self._convert_int_value_to_hex_bytes(data_type, value)
        elif "DT_CHUNK" in data_type:
            length = int(re.search("[0-9]+", data_type).group(0))
            bytes = []
            for i in range(length):
                if i < len(value):
                    bytes.append("0x%02X" % ord(value[i]))
                else:
                    bytes.append("0x00")
        else:
            raise ValueError("Unkown data_type %s" % data_type)

        self.set_data(alias, did, *bytes)

    def _get_did_by_selector(self, alias, selector, param):
        if isinstance(selector, basestring):
            try:
                selector = int(selector, 16)
            except ValueError:
                raise ValueError("Invalid selector: %s" % selector)

        dsid = self.hwfile.get_dsid_by_ypname(param)
        did = (selector << 16) | dsid

        return did

    def get_data_yp(self, alias, selector, param):
        if not self.hwfile:
            raise RuntimeError("No hardware ID file")

        did = self._get_did_by_selector(alias, selector, param)
        value = self.get_data_formatted(alias, did)

        if self.hwfile.ypname_is_enumerated(param):
            value = self.hwfile.ypenum_value2key(param, value)

        return value

    def get_idx_data_yp(self, alias, selector, idx, param):
        if not self.hwfile:
            raise RuntimeError("No hardware ID file")

        did = self._get_did_by_selector(alias, selector, param)
        if isinstance(idx, basestring):
            idx = int(idx, 16)
        value = self.get_data_formatted(alias, did, idx)

        if self.hwfile.ypname_is_enumerated(param):
            value = self.hwfile.ypenum_value2key(param, value)

        return value

    def set_data_yp(self, alias, selector, param, value):
        if not self.hwfile:
            raise RuntimeError("No hardware ID file")

        did = self._get_did_by_selector(alias, selector, param)
        if self.hwfile.ypname_is_enumerated(param):
            value = self.hwfile.ypenum_key2value(param, value)

        self.set_data_formatted(alias, did, value)

    def _get_did_by_aid(self, alias, aid, param):
        try:
            selector = self.aid_dicts[alias][aid]
        except KeyError:
            raise ValueError("Invalid AID: %s" % aid)

        return self._get_did_by_selector(alias, selector, param)

    def get_entity_param(self, alias, aid, param):
        if not self.hwfile:
            raise RuntimeError("No hardware ID file")

        did = self._get_did_by_aid(alias, aid, param)
        value = self.get_data_formatted(alias, did)

        if self.hwfile.ypname_is_enumerated(param):
            value = self.hwfile.ypenum_value2key(param, value)

        return value

    def set_entity_param(self, alias, aid, param, value):
        if not self.hwfile:
            raise RuntimeError("No hardware ID file")

        did = self._get_did_by_aid(alias, aid, param)
        if self.hwfile.ypname_is_enumerated(param):
            value = self.hwfile.ypenum_key2value(param, value)

        self.set_data_formatted(alias, did, value)
