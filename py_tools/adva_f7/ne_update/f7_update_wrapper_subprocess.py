#! /usr/bin/env python

import subprocess
import sys, time
import paramiko
import f7_update_get_load

# NE_IP = ['10.16.24.16', '10.16.24.20', '10.16.24.30', '10.16.24.254']
# NE_IP = ['10.16.23.100']
NE_IP = ['10.16.24.30', '10.16.23.100']
NE_USER, NE_PASS = ('root', 'CHGME.1')
F7SSH_PY = 'f7_ssh_io.py'
UPDATE_WRAPPER = 'f7_update_wrapper'    # filename of the update wrapper
F7_UPDATE_WRAPPER = '/tmp/f7_update_wrapper'    # the location on the NE to put UPDATE_WRAPPER

# to get info about the load
serverip, server_user, server_pwd, load_name = f7_update_get_load.get_load(sys.argv)

# to make f7_update_wrapper
with open(UPDATE_WRAPPER, 'w') as f:
    f.write('#! /bin/sh\n\n')
    f.write('FSP_WRAPPER="/usr/sbin/fsp_update_wrapper"\n')
    f.write('IP="' + serverip + '"\n')
    f.write('USER="' + server_user + '"\n')
    f.write('PASSWORD="' + server_pwd + '"\n')
    f.write('FILE="' + load_name + '"\n\n')
    f.write('${FSP_WRAPPER} ${IP} ${USER} ${PASSWORD} ${FILE}\n')

print('-----------------------------------')
# to put f7_update_wrapper on each node
for ip in NE_IP:
    # connect to the node
    i = 1
    while True:
        print("Trying to connect to %s, trial %d/30" %(ip, i))

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
            print("Could not SSH to %s. Waiting for it to start." %ip)
            i += 1
            time.sleep(2)

        # If we could not connect within time limit
        if i == 30:
            print("Could not connect to %s. Give up." %ip)
            sys.exit(1)

    # put f7_update_wrapper to the node
    f7_sftp = f7_ssh.open_sftp()
    f7_sftp.put(UPDATE_WRAPPER, F7_UPDATE_WRAPPER)
    f7_sftp.close()
    f7_cmd = 'chmod +x ' + F7_UPDATE_WRAPPER
    f7_ssh.exec_command(f7_cmd)

    print("Command done, closing SSH connection to %s\n" %ip)
    f7_ssh.close()

print('-----------------------------------')
print('New terminals opened to upgrade for each node.')

for ip in NE_IP:
    cmd = sys.executable + ' ' + F7SSH_PY + ' ' + ip + ' ' + F7_UPDATE_WRAPPER
    subprocess.call(['x-terminal-emulator', '-e', cmd])
