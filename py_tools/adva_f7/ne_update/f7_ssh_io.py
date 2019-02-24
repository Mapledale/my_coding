#! /usr/bin/env python
'''
This module is to establish an SSH connection to a node, 
send and receive strings with it.
'''
import sys
import threading, paramiko

class MySsh:
    shell = None
    client = None
    transport = None

    def __init__(self, address, username, password):
        print("Connecting to server on %s" %(str(address)))
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(address, username=username, password=password, look_for_keys=False)
        self.transport = paramiko.Transport((address, 22))
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
            print("Shell not opened!")

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
                #print(strdata, end = "")
                print(strdata),
                if (strdata.endswith("$ ")):
                    #print("\n$ ", end = "")
                    print("\n$ "),

def main(ip, cmd):
    neUser = 'root'
    nePass = 'CHGME.1'

    conn2F7 = MySsh(ip, neUser, nePass)
    conn2F7.openShell()
    conn2F7.sendShell(cmd)
    while True:
        conn2F7.process()

if __name__ == '__main__':
    ip = sys.argv[1]
    cmd = sys.argv[2]
    main(ip, cmd)


