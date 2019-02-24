#! /usr/bin/env python
# _*_ coding: utf-8

# from F7SshLibrary import F7SshSession
from pexpect.pxssh import pxssh


def main():
    ip = '10.16.24.20'
    user = 'root'
    passwd = 'CHGME.1'

    # my_f7_ssh = F7SshSession(ip, user, passwd)
    # my_f7_ssh.logout()
    s = pxssh()
    s.login(ip, user, passwd)
    s.sendline('uptime')
    s.prompt()
    print(s.before)
    s.sendline('who')
    s.prompt()
    print(s.before)
    s.logout()
    s.close()


if __name__ == '__main__':
    main()
