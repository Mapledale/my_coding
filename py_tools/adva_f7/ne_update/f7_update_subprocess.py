#! /usr/bin/env python

import os, sys
from subprocess import Popen, PIPE
import paramiko, threading
from ftplib import FTP

NE_IP = ['10.16.24.16', '10.16.24.20', '10.16.24.30', '10.16.24.254']
NE_USER, NE_PASS = ('root', 'CHGME.1')
FSP_WRAPPER = '/usr/sbin/fsp_update_wrapper'

class MySsh:
    shell = None
    client = None
    transport = None

    def __init__(self, ip, username, password, pipe_id):
        self.pipe_id = pipe_id
        #print("Connecting to server on %s" %ip)
        with open(self.pipe_id, 'w') as p:
            p.write("Connecting to server on %s\n" %ip)
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(ip, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((ip, 22))
        self.transport.connect(username=username, password=password)
        
        thread = threading.Thread(target=self.process)
        thread.daemon = True
        thread.start()
        
    def closeConnection(self):
        if (self.client != None):
            self.client.close()
            self.transport.close()
    
    def openShell(self):
        self.shell = self.client.invoke_shell()

    def sendShell(self, command):
        if (self.shell):
            self.shell.send(command + "\n")
        else:
            #print("Shell not opened!")
            with open(self.pipe_id, 'w') as p:
                p.write("Shell not opened!\n")

    def process(self):
        global connection
        while True:
            # Print data when available
            if self.shell != None and self.shell.recv_ready():
                alldata = self.shell.recv(1024)
                while self.shell.recv_ready():
                    alldata += self.shell.recv(1024)
                #strdata = str(alldata, "utf8")
                strdata = str(alldata)
                strdata.replace('\r', '')
                #print(strdata, end = "") # for python3
                #print(strdata),
                with open(self.pipe_id, 'w') as p:
                    p.write(strdata)
                if (strdata.endswith("$ ")):
                    #print("\n$ ", end = "") # for python3
                    #print("\n$ "),
                    with open(self.pipe_id, 'w') as p:
                        p.write("\n$ ")


class F7NeUpgrade(threading.Thread):
    def __init__(self, ip, cmd):
        threading.Thread.__init__(self)
        self.ip = ip
        self.cmd = cmd
        
    def run(self):
        self.pipe_path = 'my_pipe' + self.ip
        
        if not os.path.exists(self.pipe_path):
            os.mkfifo(self.pipe_path)
            
        Popen(['x-terminal-emulator', '-e', 'tail -f %s' %self.pipe_path])
        conn2F7 = MySsh(self.ip, NE_USER, NE_PASS, self.pipe_path)
        conn2F7.openShell()
        conn2F7.sendShell(self.cmd)
        while True:
            conn2F7.process()

def main():
    l_argv = len(sys.argv)
    
    # to pick the load server
    print('-----------------------------------')
    print("Which load server to use?")

    while True:
        # print("1: 172.26.2.20 (Berlin server)\t2: 172.27.3.8 (Gdy server)\n"
        #      "3: 172.16.8.154 (Atl server)\t4: 172.16.8.156 (Atl server)\n"
        #      "5: 172.27.3.16")
        print("1: 172.27.3.16 (Gdy server)\t"
              "2: 172.16.8.154 (Atl server)\n")
        
        if l_argv > 1:
            load_server_num = sys.argv[1]
            print('You picked %s' %load_server_num)
        else:
            load_server_num = str(input("Please pick from 1 to 2: "))
            
        if load_server_num == '1':
            serverip = '172.27.3.16'
            server_user = 'smoker'
            server_pwd = 'smoker'
            release_folder = '/nesw_loads/release/'
            mainline_folder = '/nesw_loads/mainline/ci/'
            break
        elif load_server_num == '2':
            serverip = '172.16.8.154'
            server_user = 'targets'
            server_pwd = 'targets'
            release_folder = '/nesw_loads/release/'
            mainline_folder = '/nesw_loads/mainline/ci/'
            break
        #    elif load_server_num == '3':
        #        serverip = '172.16.8.156'
        #        server_user = 'targets'
        #        server_pwd = 'targets'
        #        release_folder = '/releases/f7mirror/nesw_loads/release/'
        #        mainline_folder = '/releases/f7mirror/nesw_loads/mainline/ci/'
        #        break
        else:
            print("Wrong pick!\nPlease try again!\n")
    print('\n')
    
    # to determine the file_dir
    while True:
        print("How do you like to upgrade?")
        print("1: Take a specific load (full path)\t\n"
              "2: Take a specific Release load\t\t\t3: Take the LATEST Release load\n"
              "4: Take a specific Mainline load\t\t5: Take the LATEST Mainline load\n")
        
        if l_argv > 2:
            load_dir_num = sys.argv[2]
            print('You picked %s' %load_dir_num)
        else:
            load_dir_num = str(input("Please pick from 1 to 5: "))
    
        if load_dir_num == '1':
            if l_argv > 3:
                file_dir = sys.argv[3]
                print('You provided path of the CON file: %s' %file_dir)
            else:
                while True:
                    file_dir = input("Enter the path of the CON file: ")
                    if file_dir[-1] != '/':
                        file_dir += '/'
                        print('Modified file path: ', file_dir)
                        repeat = input('Hit y to continue, n to re-enter the path: ')
                        if repeat.casefold() == 'y':
                            break
                    else:
                        break        
    
            print('\nFetching the CON file from the load server...')
            myftp = FTP(serverip, server_user, server_pwd)
            myftp.cwd(file_dir)
            file_name = myftp.nlst('*.CON')
            file_name = file_name[0]
            load_name = file_dir + file_name
            myftp.quit()
    
            print('The CON file is %s' %load_name)
            break
    
        elif load_dir_num == '2':
            release = input("Enter the release number, e.g. 'r16.2.1': ")
            buildnum = input("Enter the build number, e.g. '201': ")
            file_dir = release_folder + release + '/ci/' + buildnum + '/'
    
            print('\nFetching the CON file from the load server...')
            myftp = FTP(serverip, server_user, server_pwd)
            myftp.cwd(file_dir)
            file_name = myftp.nlst('*.CON')
            file_name = file_name[0]
            load_name = file_dir + file_name
            myftp.quit()
    
            print('The CON file is %s' %load_name)
            break
    
        elif load_dir_num == '3':
            release = input("Enter the release number, e.g. 'r16.2.1': ")
            file_dir = release_folder + release + '/ci/'
    
            print('\nFetching the CON file from the load server...')
            myftp = FTP(serverip, server_user, server_pwd)
            myftp.cwd(file_dir)
            load_name_link = []
            myftp.dir('*.CON', load_name_link.append)
            load_name_link = load_name_link[0]
            load_name = load_name_link.split('->')[1].strip()
            myftp.quit()
    
            print('The CON file is %s' %load_name)
            break
    
        elif load_dir_num == '4':
            buildnum = input("Enter the build number, e.g. '201': ")
            file_dir = mainline_folder + buildnum + '/'
    
            print('\nFetching the CON file from the load server...')
            myftp = FTP(serverip, server_user, server_pwd)
            myftp.cwd(file_dir)
            file_name = myftp.nlst('*.CON')
            file_name = file_name[0]
            load_name = file_dir + file_name
            myftp.quit()
    
            print('The CON file is %s' %load_name)
            break
    
        elif load_dir_num == '5':
            file_dir = mainline_folder
    
            print('\nFetching the CON file from the load server...')
            myftp = FTP(serverip, server_user, server_pwd)
            myftp.cwd(file_dir)
            load_name_link = []
            myftp.dir('*.CON', load_name_link.append)
            load_name_link = load_name_link[0]
            # print('the link is:', load_name_link)
            load_name = load_name_link.split('->')[1].strip()
            # the GDY server has wrong link: '2latest_load.CON -> /nesw_loads//mainline/ci/11487/F7016021MXD_2017_02_23_1730.CON'
            load_name = load_name.replace('//', '/')
            myftp.quit()
    
            print('The CON file is %s' %load_name)
            break
    
        else:
            print("Wrong pick!\nPlease try again: ")
    print('\n')
    
    print('New terminals opened to upgrade for each node.')
    
    upgrade_rst = []
    for ip in NE_IP:
        cmd = FSP_WRAPPER + ' ' + serverip + ' ' + server_user + ' ' + server_pwd + ' ' + load_name
        
        ne = F7NeUpgrade(ip, cmd)
        upgrade_rst.append(ne)
        ne.start()
        
    for rst in upgrade_rst:
        rst.join(20)
        ip = rst.ip
        print('Node %s is upgrading!' %ip)
        
    print('All nodes are upgraded')
    sys.exit(0)
    
if __name__ == '__main__':
    main()
