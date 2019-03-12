#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-13 13:02:35

from AosCLILibrary import AosCLILibrary


class AutoChaseNe(object):
    USER = 'admin'
    PWD = 'CHGME.1a'
    FILTER_TYPE = ['fd-48e', 'fd-128', '40csm-', '96csm-']

    def __init__(self, ip, shelf, slot, port='n'):
        self.ip = ip
        self.ptp_start = '%s/%s/%s' % (shelf, slot, port)
        self._cli = AosCLILibrary()
        self._cli.cli_open_connection_and_login(ip, self.USER, self.PWD)
        print('Connected to node %s!\n' % ip)

    def __del__(self):
        self._cli.cli_close_connection()
        print('\nDisconnected from node %s!' % self.ip)

    def get_ptp_chain(self):
        pass

    def _get_fiber_map(self):
        '''Return a fiber trace of a given ne, from the given ptp
        1. show fiber map
        admin@Atl-15> show fiber

        fiber table:

        link-name        a-end      z-end
        1/5/n:1/1/c      1/5/n      1/1/c
        1/ext-2/n:1/5/c  1/ext-2/n  1/5/c

        '''
        return self._cli.cli_command('show fiber').cli_attrs

    def is_filter(self, card):
        card_type = self._get_card_type(card)
        for f in self.FILTER_TYPE:
            if f in card_type:
                return True
        return False

    def _get_card_type(self, card):
        '''2. show card type
        admin@Atl-15> show card 1/5

        card 1/5 table:

        item      name       part-number    admin  description
        card 1/5  am-s20h-2  1063804122-01  is     Optical Amplifier, 20dBm

        '''
        cmd = 'show card %s' % card
        card_type = self._cli.cli_command(cmd).cli_data
        card_type = card_type['card %s' % card]['name']
        return card_type

    def _get_ptp_power(self, ptp):
        '''3. to get power info
        admin@Atl-15> show interface 1/5/c opt-phy pm current

        current: [
          monitored-entity: node 1 interface 1/5/c opt-phy pm
          pm-profile: nint-IFAM20cl
          interval-size: live
          suspect-status: not-suspect
          elapsed-time: 13631 seconds
          pm-data:
            opt-rx-pwr: -1.8 dBm
            opt-tx-pwr: 20.6 dBm,

          monitored-entity: node 1 interface 1/5/c opt-phy pm
          pm-profile: m15-Power
          interval-size: 15min
          suspect-status: not-suspect
          elapsed-time: 520 seconds
          pm-data:
            opt-rx-pwr-hi: -1.8 dBm
            opt-rx-pwr-lo: -1.8 dBm
            opt-rx-pwr-mean: -1.8 dBm
            opt-tx-pwr-hi: 20.6 dBm
            opt-tx-pwr-lo: 20.5 dBm
            opt-tx-pwr-mean: 20.6 dBm,

          monitored-entity: node 1 interface 1/5/c opt-phy pm
          pm-profile: day-Power
          interval-size: 24hour
          suspect-status: partial-interval
          elapsed-time: 13631 seconds
          pm-data:
            opt-rx-pwr-hi: -1.7 dBm
            opt-rx-pwr-lo: -1.8 dBm
            opt-rx-pwr-mean: -1.8 dBm
            opt-tx-pwr-hi: 20.8 dBm
            opt-tx-pwr-lo: -29.5 dBm
            opt-tx-pwr-mean: 20.3 dBm
        ]

        '''
        cmd_show_pm = 'show interface %s opt-phy pm current' % ptp
        pm = self._cli.cli_command(cmd_show_pm).cli_data
        pm_curr = pm[0]['pm-data']
        pm_curr_rx = pm_curr['opt-rx-pwr']
        pm_curr_tx = pm_curr['opt-tx-pwr']
        return (pm_curr_rx, pm_curr_tx)

    def _is_ots(self, ptp):
        '''4. search for the port with ots
        admin@Atl-15> show interface 1/1/n/ots

        interface 1/1/n/ots table:

        display-name  user-label
        1/1/n/ots     is          normal  --  <-- the port with ots

        [node 1]
        admin@Atl-15> show interface 1/5/n/ots

        Error(400): Wrong command syntax. Unknown token(s): '1/5/n/ots'.

        '''
        cmd_ots = 'show interface %s' % ptp
        comp = self._cli.cli_get_completions(cmd_ots).cli_attrs
        return '%s/ots' % ptp in comp

    def _get_next_node_ip(self, ptp):
        '''5. get to the next node - its ip address
        show interface 1/2/n/ots ots remote-ots-node

        remote-ots-node:
          remote-management-address: [
            1: 10.16.45.11, <-- ip of the next node
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
        cmd_next_ne = 'show interface %s/ots ots remote-ots-node' % ptp
        ne_next = self._cli.cli_command(cmd_next_ne).cli_data
        return ne_next['remote-management-address'][0]

    def _get_next_node_ots(self, ptp):
        '''6. get to the next node - its port with ots
        show interface 1/2/n/ots/eth mac lldp-port bridge nearest remote-node

        remote-node: [
          index: 1
          chassis-id-sub-type: chassis-component
          chassis-id: LBADVA71160804785
          port-id-sub-type: interface-name
          port-id: node 1 interface 1/2/n/ots/eth mac <-- the port with ots
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
        cmd_port_id = 'show interface %s/ots/eth mac lldp-port bridge nearest \
            remote-node' % ptp
        rsp = self._cli.cli_command(cmd_port_id).cli_data
        rsp = rsp.values()[0]['port-id']
        port_id = rsp.split('interface ')[1]
        return port_id.split('/ots')[0]


def main():
    # ip = '10.16.45.15'
    # ip = '10.16.45.14'
    ip = '10.16.45.13'
    shelf = '1'
    slot = '1'
    port = 'n'
    ne1 = AutoChaseNe(ip, shelf, slot)
    ptp = '%s/%s/%s' % (shelf, slot, port)

    # fiber_map = ne1._get_fiber_map()
    # print('fiber map:')
    # for link_name in fiber_map:
    #     print('%s' % link_name)

    # card_type = ne1._get_card_type('%s/%s' % (shelf, slot))
    # print('\nCard Type of %s/%s:' % (shelf, slot))
    # print('%s' % card_type)

    # pm = ne1._get_ptp_power(ptp)
    # print('\nPM readings of %s:' % ptp)
    # print('pm_r: %s' % pm[0])
    # print('pm_t: %s' % pm[1])

    # print('\nIs %s with ots?' % ptp)
    # print(ne1._is_ots(ptp))
    # print('Is %s with ots?' % '1/5/n')
    # print(ne1._is_ots('1/5/n'))

    # print('\nThe next node:')
    # print('ip: %s' % ne1._get_next_node_ip(ptp))
    # print('ptp with ots: %s' % ne1._get_next_node_ots(ptp))

    # cards = ['1/1', '1/5', '1/6', '1/cem', '1/ecm-1', '1/ext-2',
    #          '1/fan-1', '1/psm-3']
    # cards = ['1/1', '1/2', '1/5', '1/cem', '1/ecm-1',
    #          '1/fan-1', '1/psm-1']
    cards = ['1/1', '1/2', '1/5', '1/16', '1/cem', '1/ecm-1', '1/ext-1',
             '1/ext-2', '1/fan-1', '1/psm-1']
    for card in cards:
        print('Is card %s a filter? %s' % (card, ne1.is_filter(card)))


if __name__ == '__main__':
    main()
