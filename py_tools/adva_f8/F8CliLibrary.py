#! /usr/bin/env python
# _*_ coding: utf-8 *_*
'''
This is a library for ssh connection using pexpect
basing on TCClientLibrary
author: David Deng ddengca@gmail.com
'''

import re
import pexpect
from pexpect.pxssh import pxssh
from robot.api import logger
# from HardwareIdFile import HardwareIdFile
# from aid_convert import AID2SELECTOR_BY_MODTYPE

USE_PRINT = False

REGEX_FLAGS = re.MULTILINE | re.DOTALL

# PROMPT_PATTERN = r"([^ \n\r]+ ?> ?)$"
PROMPT_PATTERN = r"([^ \n\r]+@FSP3000C)>"
MAX_CONNECTIONS = \
    "Max. number of connections \([0-9]+\) to card [0-9]+-[0-9]+ reached."
READ_TIMEOUT = 5

DATA_TYPES_INT = ["DT_BYTE", "DT_WORD", "DT_DWORD", "DT_QWORD"]


def remove_non_printable(buffer):
    # remove ASCII escape codes
    buffer = re.sub(r"\x1b(E|[^m]*m)", "", buffer)
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


class F8CliSession(pxssh):

    def __init__(self, ipaddress,
                 username="admin", password="CHGME.1a", **kwargs):
        pxssh.__init__(self)

        self.timeout = READ_TIMEOUT

        # self.PROMPT = "[node 1]\r\nadmin@FSP3000C> "
        self.PROMPT = r"admin@FSP3000C[*]?[#>] "

        if "sync_multiplier" in kwargs:
            kwargs["sync_multiplier"] = float(kwargs["sync_multiplier"])
        else:
            kwargs["sync_multiplier"] = 4.0

        self.login(ipaddress, username,
                   password, auto_prompt_reset=False, **kwargs)
        self.prompt()
        self.before

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
