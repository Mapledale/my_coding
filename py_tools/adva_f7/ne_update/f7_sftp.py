#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  f7_ssh.py
#  
#  Copyright 2017 David Deng <ddengca@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

import sys
from time import sleep
import paramiko

NE_USER = 'root'
NE_PASS = 'CHGME.1'

def sftp_put(ip, loc_file, rmt_file):
    '''
    This method is to put <loc_file> to <rmt_file> via SFTP
    
    Example:
    sftp_put('10.16.24.16', 'f7_update_wrapper', '/tmp/f7_update_wrapper')
    '''
    # connect to the node
    trial_tot = 10
    trial_num = 1
    wait_time = 10
    while True:
        print("Trying to connect to %s, trial %d/%d" %(ip, trial_num, trial_tot))

        try:
            f7_ssh = paramiko.SSHClient()
            f7_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            f7_ssh.connect(ip, username = NE_USER, password = NE_PASS)
            print("Connected to %s" %ip)
            break
        except paramiko.AuthenticationException:
            print("Authentication failed when connecting to %s" %ip)
            sys.exit(1)
        except:
            print("Could not SSH to %s. Wait %d seconds for it to start.\n" %(ip, wait_time))
            sleep(wait_time)
            trial_num += 1

        # If we could not connect tried trial_tot times
        if trial_num > trial_tot:
            print("Could not connect to %s. Give up." %ip)
            sys.exit(1)

    # put file to the node
    f7_sftp = f7_ssh.open_sftp()
    f7_sftp.put(loc_file, rmt_file)
    f7_sftp.close()
    #f7_ssh.exec_command("chmod +x /tmp/f7_update_wrapper")

    print("Command done, closing SSH connection to %s\n" %ip)
    f7_ssh.close()

def main():
    pass

if __name__ == '__main__':
    ip = sys.argv[1]
    src = sys.argv[2]
    dest = sys.argv[3]
    sftp_put(ip, src, dest)
    
