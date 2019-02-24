#! /usr/bin/env python
# _*_ coding: utf-8

'''
F8 ssh trial script
using F8CliLibrary, basing on pexpect
'''

from F8CliLibrary import F8CliSession


def main():
    ip = '172.16.37.22'
    user = 'admin'
    passwd = 'CHGME.1a'

    my_f8_ssh = F8CliSession(ip, user, passwd)

    # cmd = 'show card 1/18'
    # my_f8_ssh.sendline(cmd)
    # my_f8_ssh.prompt()
    # resp = my_f8_ssh.before
    # print(resp)

    cmd = 'configure'
    my_f8_ssh.sendline(cmd)
    # my_f8_ssh.prompt()
    # resp = my_f8_ssh.before
    # print(resp)

    cmd = 'set card 1/18 admin oos'
    my_f8_ssh.sendline(cmd)
    # my_f8_ssh.prompt()
    # resp = my_f8_ssh.before
    # print(resp)

    cmd = 'commit'
    my_f8_ssh.sendline(cmd)
    # my_f8_ssh.prompt()
    # resp = my_f8_ssh.before
    # print(resp)

    # cmd = 'history'
    # my_f8_ssh.sendline(cmd)
    # my_f8_ssh.prompt()
    # resp = my_f8_ssh.before
    # print(resp)

    cmd = 'exit'
    my_f8_ssh.sendline(cmd)
    # my_f8_ssh.prompt()
    # resp = my_f8_ssh.before
    # print(resp)

    my_f8_ssh.logout()


if __name__ == '__main__':
    main()
