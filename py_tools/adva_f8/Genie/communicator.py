# from pywinauto.application import Application
# pip install pywinauto
import time
import os
import json

# autoinstall libraries
try:

    from pywinauto.application import Application

    print"imported pywinauto "
except:
    try:
        os.system('pip install pywinauto')
        print"installed pywinauto"
        from pywinauto.application import Application
    except:
        # print 'linux detected'
        None
try:
    import AosLibrary

    print"imported AosLibrary "
except:
    try:
        print 'output: ' + str(
            os.system('pip install -i https://pypi.rd.advaoptical.com/global/production robotframework'))
        print 'output: ' + str(
            os.system('pip install -i https://pypi.rd.advaoptical.com/global/production robotframework-aoslibrary'))
        print"installed AosLibrary"
        print 'output: ' + str(
            os.system('pip install -i https://pypi.rd.advaoptical.com/global/production robotframework-aosdtelibrary'))
        print"installed AosDTELibrary"
        os.system('pip install -i https://pypi.rd.advaoptical.com/global/production robotframework-aosclilibrary')
        print"installed AosCLILibrary"
        import AosLibrary
    except:
        print 'output: ' + str(
            os.system('sudo pip install -i https://pypi.rd.advaoptical.com/global/production robotframework'))
        print 'output: ' + str(
            os.system(
                'sudo pip install -i https://pypi.rd.advaoptical.com/global/production robotframework-aoslibrary'))
        print"installed AosLibrary"
    import AosLibrary

try:
    import AosDTELibrary

    print"imported AosDTELibrary "
except:
    try:
        print 'output: ' + str(
            os.system('pip install -i https://pypi.rd.advaoptical.com/global/production robotframework-aosdtelibrary'))
        print"installed AosDTELibrary"
        import AosDTELibrary
    except:
        print 'output: ' + str(os.system(
            'sudo pip install -i https://pypi.rd.advaoptical.com/global/production robotframework-aosdtelibrary'))
    print "installed AosDTELibrary"
    import AosDTELibrary
try:
    import AosCLILibrary

    print"imported AosCLILibrary "
except:
    try:
        os.system('pip install -i https://pypi.rd.advaoptical.com/global/production robotframework-aosclilibrary')
        print"installed AosCLILibrary"
        import AosCLILibrary
    except:
        os.system('sudo pip install -i https://pypi.rd.advaoptical.com/global/production robotframework-aosclilibrary')
    print"installed AosCLILibrary"
    import AosCLILibrary

try:
    import SSHLibrary

    print"imported SSHLibrary "
except:
    try:
        os.system('pip install SSHLibrary')
        print"installed SSHLibrary"
        import SSHLibrary
    except:
        os.system('pip install SSHLibrary')
    print"installed SSHLibrary"
    import SSHLibrary

'''
import AosLibrary
import AosDTELibrary
import AosCLILibrary
import SSHLibrary
'''


class TerminalConnector:
    putty = None

    def __init__(self, os):
        self.os = os
        print 'os: ' + os
        if os!='win':
            '''try:
                os.system('sshpass ')
            except:
                print 'fail'
                os.system('sudo yum -y install sshpass ')
            '''
        self.aoslib = AosLibrary.AosLibrary()
        self.cli = AosCLILibrary.AosCLILibrary()
        self.dte = AosDTELibrary.AosDTELibrary()
        self.ssh = SSHLibrary.SSHLibrary()
        # self.ecm_ip = '10.16.45.17'

    def prepareString(self, string):
        return string.replace(' ', '{SPACE}')

    def openSSHSession(self, host, username='admin', password='CHGME.1a', port='22'):
        if self.os == 'win':
            app = Application().start(cmd_line=u'putty -ssh ' + username + '@' + host + ' ' + port)
            self.putty = app.PuTTY
            self.putty.wait('ready')
            time.sleep(1)
            self.putty.type_keys(password)
            self.putty.type_keys("{ENTER}")
        else:
            os.system('gnome-terminal -x sshpass -p ' + password + ' ssh ' + username + '@' + host)
            print 'gnome-terminal -x sshpass -p ' + password + ' ssh ' + username + '@' + host

    def openDTESession(self, host, username='root', password='', port='614'):
        if self.os == 'win':
            app = Application().start(cmd_line=u'putty -ssh ' + username + '@' + host + ' ' + port)
            self.putty = app.PuTTY
            self.putty.wait('ready')
            time.sleep(1)
            self.putty.type_keys(password)
        else:
            os.system('gnome-terminal -x  ssh -p 614 ' + username + '@' + host)

    def getLogs(self, host, username='admin', password='CHGME.1a', port='22'):
        if self.os == 'win':
            app = Application().start(cmd_line=u'putty -ssh ' + username + '@' + host + ' ' + port)
            self.putty = app.PuTTY
            self.putty.wait('ready')
            time.sleep(1)
            self.putty.type_keys(password)
            self.putty.type_keys("{ENTER}")
        else:
            print 'TODO'

    def openTelnetSession(self, host, username='admin', password='CHGME.1a', port='23'):
        if self.os == 'win':
            app = Application().start(cmd_line=u'putty -telnet ' + username + '@' + host + ' ' + port)
            self.putty = app.PuTTY
            self.putty.wait('ready')
            time.sleep(1)
            self.putty.type_keys(username)
            self.putty.type_keys("{ENTER}")
            time.sleep(1)
            self.putty.type_keys(password)
            self.putty.type_keys("{ENTER}")
            time.sleep(1)
            self.putty.type_keys(self.prepareString('conf'))
            self.putty.type_keys("{ENTER}")
            time.sleep(1)
            self.putty.type_keys(
                self.prepareString('set security user-settings admin cli-user-settings session-idle-timeout 0'))
            self.putty.type_keys("{ENTER}")
            time.sleep(1)
            self.putty.type_keys(self.prepareString('commit'))
            self.putty.type_keys("{ENTER}")
            time.sleep(1)
            self.putty.type_keys(self.prepareString('exit'))
            self.putty.type_keys("{ENTER}")
        else:
            print 'Not implemented'

        # Getting ipv6 address of teh module

    def get_ipv6(self, ecm_ip):
        self.dte.dcli_open_connection_and_login(ecm_ip)
        self.dte.dcli_go('debug')
        self.dte.dcli_go('aosCoreTd')
        slot_ipv6 = {}
        Topology = self.dte.dcli_command_with_raw_output('getTopologyTree')
        Topology = json.loads(Topology)
        # import ipdb
        # ipdb.set_trace()
        self.slotShelf = []

        # for i in range(len(Topology['pload'][0]['value'])) :
        modulelists = Topology['pload'][0]['value'][0]['cards']

        for slot in modulelists:
            sl = slot['slot']
            ipv6 = slot['ipv6']
            role = slot['role']
            if sl > 20 and role == 'CC':
                sl = 'CEM'
            if role == 'EC':
                sl = 'ECM'
                ipv6 = ecm_ip

            try:
                slot_ipv6[sl].append(ipv6)

            except KeyError:
                slot_ipv6[sl] = [ipv6]

        self.aoslib.close_all_sessions()

        return slot_ipv6

    def factoryReset(self, ecm_ip):
        self.aoslib.open_session('REST', ecm_ip, 'admin', 'CHGME.1a', product='f8', release='master')
        self.cli.cli_open_connection_and_login(ecm_ip, 'admin', 'CHGME.1a')
        # RTF
        fqdn = '/me=1/mgt'
        self.aoslib.execute(fqdn, 'resfct')
        self.aoslib.close_all_sessions()

    def reboot(self, ecm_ip, slot=1, option='warm'):
        self.aoslib.open_session('REST', ecm_ip, 'root', 'CHGME.1a', product='f8', release='master')
        self.dte.dcli_open_connection_and_login(ecm_ip)
        self.aoslib.execute('/me=1/eqh=shelf,1/eqh=slot,' + str(slot) + '/eq=card/card', option)
        self.aoslib.close_all_sessions()

    def openSSHToNode(self, host, node, username='root', password='', port='614'):
        if self.os == 'win':
            app = Application().start(cmd_line=u'putty -ssh ' + username + '@' + host + ' ' + port)
            self.putty = app.PuTTY
            self.putty.wait('ready')
            time.sleep(1)
            self.putty.type_keys(password)
            time.sleep(0.1)
            self.putty.type_keys(self.prepareString('ssh ' + str(node) + '{%}mgmt'))
            self.putty.type_keys("{ENTER}")
        else:
            os.system('gnome-terminal -x  ssh -t -p 614 ' + username + '@' + host + ' ssh ' + str(node) + '%mgmt ')
            print 'TODO'

    def getInfo(self, ecm_ip, slots):
        # ecm_ip = '10.16.45.16'
        try:
            self.aoslib.open_session('REST', ecm_ip, 'admin', 'CHGME.1a', product='f8', release='master')
            self.cli.cli_open_connection(ecm_ip)
            self.cli.cli_open_connection_and_login(ecm_ip, 'admin', 'CHGME.1a')
            # a = self.aoslib.read_all_params('/me=1/eqh=shelf,1/eqh=slot,ecm-1/eq=card/card/sw/active/pkg')

            ret = []
            # try:
            print slots
            for slot in slots:
                # print slot
                # slotVers = self.aoslib.read_all_params('/me=1/eqh=shelf,1/eqh=slot,1/eq=card/card/sw/active/pkg')
                if slot == 'ECM':
                    slotVers = self.aoslib.read_all_params('/me=1/eqh=shelf,1/eqh=slot,ecm-1/eq=card/card/sw/active/pkg')
                elif slot == 'CEM':
                    slotVers = self.aoslib.read_all_params('/me=1/eqh=shelf,1/eqh=slot,cem/eq=card/card/sw/active/pkg')
                elif 'Local' in str(slot):
                    None
                else:
                    print slot
                    # import ipdb
                    # ipdb.set_trace()
                    slotVers = self.aoslib.read_all_params(
                        '/me=1/eqh=shelf,1/eqh=slot,' + str(slot) + '/eq=card/card/sw/active/pkg')
                    # print slotVers
                try:
                    if 'f8-cc' in slotVers['result'][0]['dnm']:
                        res = slotVers['result'][1]
                    else:
                        res = slotVers['result'][0]
                    id = res['id']
                    dnm = res['dnm']
                    ret.append({'id': id, 'dnm': dnm})
                except:
                    None
                # print res

            # print id
            # print dnm
            self.aoslib.close_all_sessions()
        except:
            ret=[]
        return ret

    def core(self, host, module):

        if ':' in module:
            self.ssh.open_connection(host, port=614, prompt='#')
            self.ssh.login('root', '')
            self.ssh.write('ssh -o \"StrictHostKeyChecking no\" ' + str(module) + '%mgmt ')
        elif 'Local' in module:
            None
        else:

            self.ssh.open_connection(host, port=614, prompt='#')
            self.ssh.login('root', '')
        self.ssh.write('/bin/ls -1 /tmp/core.* 2>/dev/null')
        all_core_name = self.ssh.read_until('#')
        all_core_name = all_core_name.replace('\n.*\#', "", 1)
        all_core_name = all_core_name.replace('ecm.*\#', "", 100)
        all_core_name = all_core_name.replace('\#\\*\#', "", 100)
        core_name = [all_core_name.split()]
        print 'Core of card at: ' + module
        print core_name
        print '~~~~~'
        print all_core_name
        print '!!!!!!'

    def scp(self, src, dest, srcPath, destPath, ecm_ip):
        tempPath = '/tmp/genie/'
        self.ssh.open_connection(ecm_ip, port=614)
        self.ssh.login('root', '')
        self.ssh.write('mount -o remount,rw /opt/adva')
        if self.os == 'win':
            if ':' in dest or ':' in src:
                # ipv6 -> to card -> hop over ecm
                # mkdir genie

                self.ssh.write(
                    'ssh -o \"StrictHostKeyChecking no\" root@[' + dest + '%mgmt] mount -o remount,rw /opt/adva')

                if '/' in srcPath:
                    filename = srcPath.split('/')[-1]
                elif '\\' in srcPath:
                    filename = srcPath.split('\\')[-1]
                else:
                    print 'error parsing source string'
                    return

                print filename
                print 'ipv6 area'

                if src == dest:
                    print 'Nothing to do'
                elif src == '':
                    # scp from local to ecm then from ecm to dest
                    self.ssh.write('mkdir ' + tempPath)
                    os.system('pscp -scp  -P 614 ' + srcPath + ' root@' + ecm_ip + ':' + tempPath)
                    self.ssh.write('scp -6  ' + tempPath + filename + ' root@[' + dest + '%mgmt]:' + destPath)
                    print 'scp -6  ' + tempPath + filename + ' root@[' + dest + '%mgmt]:' + destPath
                elif dest == '':
                    # scp from src to ecm then scp from ecm to local
                    self.ssh.write('mkdir ' + tempPath)
                    self.ssh.write('scp -6 root@[' + dest + '%mgmt]:' + srcPath + ' ' + tempPath)
                    os.system('pscp -scp  -P 614 root@' + ecm_ip + ':' + tempPath + filename + ' ' + destPath)
                    print 'pscp -scp -P 614 root@' + src + ':' + srcPath + ' ' + destPath
                elif ':' in src and ':' in dest:
                    self.ssh.write(
                        'scp -6 root@[' + src + '%mgmt]:' + srcPath + ' root@[' + dest + '%mgmt]:' + destPath)
                elif ':' in src:
                    # ssh to ecm_ip scp from src to ecm
                    self.ssh.write('scp -6 root@[' + src + '%mgmt]:' + srcPath + ' ' + destPath)
                    print 'copied from card to ecm: ' + 'scp -6 root@[' + src + '%mgmt]:' + srcPath + ' ' + destPath

                elif ':' in dest:
                    # ssh to ecm_ip scp from ecm to dest
                    self.ssh.write('scp -6  ' + srcPath + ' root@[' + dest + '%mgmt]:' + destPath)
                    print 'copied from ecm to card: ' + 'scp -6  ' + srcPath + ' root@[' + dest + '%mgmt]:' + destPath
                else:
                    print 'invalid'

            else:
                # ipv4 -> ecm

                if src == dest:
                    print 'Nothing to do'
                elif src == '':
                    os.system('pscp -scp  -P 614 ' + srcPath + ' root@' + dest + ':' + destPath)
                    print 'pscp -scp  -P 614 ' + srcPath + ' root@' + dest + ':' + destPath
                elif dest == '':
                    os.system('pscp -scp -P 614 root@' + src + ':' + srcPath + ' ' + destPath)
                    print 'pscp -scp -P 614 root@' + src + ':' + srcPath + ' ' + destPath

                else:
                    print 'invalid'
        else:

            if ':' in dest or ':' in src:
                # ipv6 -> to card -> hop over ecm
                # mkdir genie

                self.ssh.write(
                    'ssh -o \"StrictHostKeyChecking no\" root@[' + dest + '%mgmt] mount -o remount,rw /opt/adva')

                if '/' in srcPath:
                    filename = srcPath.split('/')[-1]
                elif '\\' in srcPath:
                    filename = srcPath.split('\\')[-1]
                else:
                    print 'error parsing source string'
                    return

                print filename
                print 'ipv6 area'

                if src == dest:
                    print 'Nothing to do'
                elif src == '':
                    # scp from local to ecm then from ecm to dest
                    self.ssh.write('mkdir ' + tempPath)
                    os.system('scp  -P 614 ' + srcPath + ' root@' + ecm_ip + ':' + tempPath)
                    self.ssh.write('scp -6  ' + tempPath + filename + ' root@[' + dest + '%mgmt]:' + destPath)
                    print 'done scp from local to ecm then from ecm to dest'
                elif dest == '':
                    # scp from src to ecm then scp from ecm to local
                    self.ssh.write('mkdir ' + tempPath)
                    self.ssh.write('scp -6 root@[' + dest + '%mgmt]:' + srcPath + ' ' + tempPath)
                    os.system('scp  -P 614 root@' + ecm_ip + ':' + tempPath + filename + ' ' + destPath)
                    print 'done scp from src to ecm then scp from ecm to local'
                elif ':' in src and ':' in dest:
                    self.ssh.write(
                        'scp -6 root@[' + src + '%mgmt]:' + srcPath + ' root@[' + dest + '%mgmt]:' + destPath)
                elif ':' in src:
                    # ssh to ecm_ip scp from src to ecm
                    self.ssh.write('scp -6 root@[' + src + '%mgmt]:' + srcPath + ' ' + destPath)
                    print 'copied from card to ecm: ' + 'scp -6 root@[' + src + '%mgmt]:' + srcPath + ' ' + destPath

                elif ':' in dest:
                    # ssh to ecm_ip scp from ecm to dest
                    self.ssh.write('scp -6  ' + srcPath + ' root@[' + dest + '%mgmt]:' + destPath)
                    print 'copied from ecm to card: ' + 'scp -6  ' + srcPath + ' root@[' + dest + '%mgmt]:' + destPath
                else:
                    print 'invalid'

            else:
                # ipv4 -> ecm

                if src == dest:
                    print 'Nothing to do'
                elif src == '':
                    os.system('scp  -P 614 ' + srcPath + ' root@' + dest + ':' + destPath)
                    print 'scp  -P 614 ' + srcPath + ' root@' + dest + ':' + destPath
                elif dest == '':
                    os.system('scp -P 614 root@' + src + ':' + srcPath + ' ' + destPath)
                    print 'scp -P 614 root@' + src + ':' + srcPath + ' ' + destPath

                else:
                    print 'invalid'

# C:\Users\simonbu\Documents\test.txt
