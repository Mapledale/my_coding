#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  f7_update_get_load.py
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

from ftplib import FTP

def fetch_load(serverip, server_user, server_pwd, file_dir):
    myftp = FTP(serverip, server_user, server_pwd)
    myftp.cwd(file_dir)
    load_name_link = []
    myftp.dir('*.CON', load_name_link.append) # the default output of FTP.dir is stdio    
    myftp.quit()
    
    load_name_link = load_name_link[0] # there should be only 1 *.CON file
    if '->' in load_name_link: # for symbol link
        load_name = load_name_link.split('->')[1].strip()
    else:
        load_name = file_dir + 'F7' + load_name_link.split('F7')[1]
    # the GDY server has wrong link: 'latest_load.CON -> /nesw_loads//mainline/ci/11487/F7016021MXD_2017_02_23_1730.CON'
    if '//' in load_name:
        load_name = load_name.replace('//', '/')

    return load_name
    
def get_load(argv):
    '''
    argv[1]: load_server_num
    argv[2]: load_dir_num
    argv[3]: file_dir, if argv[2] == '1'
             buildnum, if argv[2] == '2'
             release, if argv[2] == '4' or argv[2] == '5' or argv[2] == '6'
    argv[4]: buildnum
    '''
    l_argv = len(argv)
    
    # to pick the load server
    while True:    
        print('-----------------------------------')
        print('Which load server to use?')    
        # print("1: 172.26.2.20 (Berlin server)\t2: 172.27.3.8 (Gdy server)\n"
        #      "3: 172.16.8.154 (Atl server)\t4: 172.16.8.156 (Atl server)\n"
        #      "5: 172.27.3.16")
        print("1: 172.27.3.16 (Gdy server)\t"
              "2: 172.16.8.154 (Atl server)\n")
        
        if l_argv > 1:
            load_server_num = argv[1]
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
        #elif load_server_num == '3':
        #    serverip = '172.16.8.156'
        #    server_user = 'targets'
        #    server_pwd = 'targets'
        #    release_folder = '/releases/f7mirror/nesw_loads/release/'
        #    mainline_folder = '/releases/f7mirror/nesw_loads/mainline/ci/'
        #    break
        else:
            print("Wrong pick!\nPlease try again!\n")
    print('\n')
    
    # to determine the file_dir
    while True:
        print("How do you like to upgrade?")
        print("1: Take a specific load (full path)\n"          
              "2: Take a specific Mainline ci load\t3: Take the LATEST Mainline ci load\n"
              "4: Take a specific Release ci load\t5: Take the LATEST Release ci load\n"
              "6: Take a specific Release load\n")
        
        if l_argv > 2:
            load_dir_num = argv[2]
            print('You picked %s' %load_dir_num)
        else:
            load_dir_num = str(input("Please pick from 1 to 6: "))
    
        if load_dir_num == '1': # Take a specific load (full path)
            if l_argv > 3:
                file_dir = argv[3]
                print('You provided the path of the CON file as: %s' %file_dir)
            else:
                while True:
                    file_dir = input("Enter the path of the CON file: ")
                    if file_dir[-1] != '/':
                        file_dir += '/'
                        print('Modified file path: ', file_dir)
                        repeat = input('Hit y to continue, n to re-enter the path: ')
                        # if repeat.casefold() == 'y': # for Python 3.x only
                        if repeat == 'y':
                            break
                    else:
                        break
    
            print('\nFetching the CON file from the load server...')
            load_name = fetch_load(serverip, server_user, server_pwd, file_dir)    
            print('The CON file is %s' %load_name)
            break
            
        elif load_dir_num == '2': # Take a specific Mainline ci load
            if l_argv > 3:
                buildnum = argv[3]
                print('You provided the build number as: %s' %buildnum)
            else:
                buildnum = input("Enter the build number, e.g. '201': ")
            file_dir = mainline_folder + buildnum + '/'
    
            print('\nFetching the CON file from the load server...')
            load_name = fetch_load(serverip, server_user, server_pwd, file_dir)
            print('The CON file is %s' %load_name)
            break
            
        elif load_dir_num == '3': # Take the LATEST Mainline ci load
            file_dir = mainline_folder
    
            print('\nFetching the CON file from the load server...')
            load_name = fetch_load(serverip, server_user, server_pwd, file_dir)
            print('The CON file is %s' %load_name)
            break  
    
        elif load_dir_num == '4': # Take a specific Release ci load
            if l_argv > 4:
                release = argv[3]
                buildnum = argv[4]
                print('You provided the release number as: %s' %release)
                print('You provided the build number as: %s' %buildnum)
            else:
                release = input("Enter the release number, e.g. 'r16.2.1': ")
                buildnum = input("Enter the build number, e.g. '201': ")
            file_dir = release_folder + release + '/ci/' + buildnum + '/'
    
            print('\nFetching the CON file from the load server...')
            load_name = fetch_load(serverip, server_user, server_pwd, file_dir)
            print('The CON file is %s' %load_name)
            break
    
        elif load_dir_num == '5': # Take the LATEST Release ci load
            if l_argv > 3:
                release = argv[3]
                print('You provided the release number as: %s' %release)
            else:
                release = input("Enter the release number, e.g. 'r16.2.1': ")
            file_dir = release_folder + release + '/ci/'
    
            print('\nFetching the CON file from the load server...')
            load_name = fetch_load(serverip, server_user, server_pwd, file_dir)            
            print('The CON file is %s' %load_name)
            break
    
        elif load_dir_num == '6': # Take a specific Release load
            if l_argv > 4:
                release = argv[3]
                buildnum = argv[4]
                print('You provided the release number as: %s' %release)
                print('You provided the subfolder name as: %s' %buildnum)
            else:
                release = input("Enter the release number, e.g. 'r16.2.1': ")
                buildnum = input("Enter the subfolder name, e.g. '2017-11-16': ")
            file_dir = release_folder + release + '/' + buildnum + '/'
    
            print('\nFetching the CON file from the load server...')
            load_name = fetch_load(serverip, server_user, server_pwd, file_dir)
            print('The CON file is %s' %load_name)
            break

    return (serverip, server_user, server_pwd, load_name)

def main():
    ip = '172.27.3.16'
    user = 'smoker'
    pwd = 'smoker'
    file_dir = '/mkssi/tmp/mainline/ci/'
    #file_dir = '/releases/f7mirror/nesw_loads/release/r17.1.1/ci/44/'
    fetch_load(ip, user, pwd, file_dir)
    return 0

if __name__ == '__main__':
    main()
