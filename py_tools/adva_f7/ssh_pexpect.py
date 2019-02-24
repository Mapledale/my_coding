#! /usr/bin/env python
# _*_ coding: utf-8 _*_

'''
F8 ssh trial script
using pexpect
'''

from pexpect.pxssh import pxssh
import re


def main():
    ip = '172.16.37.22'
    user = 'admin'
    passwd = 'CHGME.1a'

    my_f8_ssh = pxssh()
    # 3 cases of prompt: 'admin@FSP3000C> ',
    # 'admin@FSP3000C# ', 'admin@FSP3000C*# '
    my_f8_ssh.PROMPT = r"admin@FSP3000C[*]?[#>] "
    my_f8_ssh.login(ip, user, passwd, auto_prompt_reset=False)
    # disable auto_prompt_reset as my_f8_ssh.PROMPT is explicitly defined
    my_f8_ssh.prompt()
    my_f8_ssh.before  # to consume the warning after login

    cmd = 'show card 1/18'
    my_f8_ssh.sendline(cmd)
    my_f8_ssh.prompt()
    resp = my_f8_ssh.before
    print(resp)
    pat = re.compile(r"is|oos")
    admin_ori = pat.search(resp).group(0)

    cmd = 'configure'  # enter configure mode
    my_f8_ssh.sendline(cmd)
    my_f8_ssh.prompt()
    resp = my_f8_ssh.before
    print(resp)

    if admin_ori == 'is':
        admin_new = 'oos'
    elif admin_ori == 'oos':
        admin_new = 'is'
    else:
        admin_new = 'bad'
    cmd = 'set card 1/18 admin ' + admin_new
    my_f8_ssh.sendline(cmd)
    my_f8_ssh.prompt()
    resp = my_f8_ssh.before
    print(resp)

    cmd = 'commit'
    my_f8_ssh.sendline(cmd)
    my_f8_ssh.prompt()
    resp = my_f8_ssh.before
    print(resp)

    cmd = 'exit'  # exit configure mode
    my_f8_ssh.sendline(cmd)
    my_f8_ssh.prompt()
    resp = my_f8_ssh.before
    print(resp)

    cmd = 'show card 1/18'
    my_f8_ssh.sendline(cmd)
    my_f8_ssh.prompt()
    resp = my_f8_ssh.before
    print(resp)

    my_f8_ssh.logout()


if __name__ == '__main__':
    main()
