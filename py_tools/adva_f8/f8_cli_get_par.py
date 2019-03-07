#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-07 16:02:35

from AosCLILibrary import AosCLILibrary


user = 'admin'
pwd = 'CHGME.1a'
ne1_ip = '10.16.45.12'
ne1_alias = 'node12'

ne1_cli = AosCLILibrary()
ne1_cli.cli_open_connection_and_login(ne1_ip, user, pwd, ne1_alias)
print('Connected to node %s!\n' % ne1_ip)


# show fiber
cmd_show_fiber = 'show fiber'
ne1_fiber_dic = ne1_cli.cli_command(cmd_show_fiber).cli_data  # at basic.py

for link_name in ne1_fiber_dic:
    a_end = ne1_fiber_dic[link_name]['a-end']
    z_end = ne1_fiber_dic[link_name]['z-end']
    print('fiber map:')
    print('link-name: %s\t' % link_name),
    print('a-end: %s\t' % a_end),
    print('z-end: %s\n' % z_end)


'''
show interface 1/2/n/ots ots remote-ots-node

remote-ots-node:
  remote-management-address: [
    1: 10.16.45.11,
    2: 127.0.0.1,
    3: 192.168.1.1,
    4: ::1,
    5: fe80::280:eaff:fe81:c0b1,
    6: fe80::280:eaff:fe82:21f0
  ]
  remote-interface-name: node 1 interface 1/2/n/ots/eth mac
  remote-node-role: node-role-ots-tt
  remote-system-name: FSP3000C
  remote-system-description:

'''
cmd_next_ne = 'show interface 1/2/n/ots ots remote-ots-node'
ne_next = ne1_cli.cli_command(cmd_next_ne).cli_data
ne_next_ip = ne_next['remote-management-address'][0]
print('The ip of next node is: %s\n' % ne_next_ip)


'''
show interface 1/2/n/ots/eth mac lldp-port bridge nearest remote-node

remote-node: [
  index: 1
  chassis-id-sub-type: chassis-component
  chassis-id: LBADVA71160804785
  port-id-sub-type: interface-name
  port-id: node 1 interface 1/2/n/ots/eth mac
  port-description:
  system-name: FSP3000C
  system-description:
  system-capability-support: []
  system-capability-enabled: []
  time-to-live: 121
  remote-changes: True
  too-many-neighbors: False
  time-stamp: 0,00:01:24.00
]

'''
cmd_port_id = \
    'show interface 1/2/n/ots/eth mac lldp-port bridge nearest remote-node'
port_id = ne1_cli.cli_command(cmd_port_id).cli_data
port_id = port_id['1']['port-id']
print('The port-id is: %s' % port_id)


# ne1_cli.cli_close_connection()
ne1_cli.cli_close_all_connections()
