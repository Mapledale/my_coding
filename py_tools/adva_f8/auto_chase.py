#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-03-13 13:02:35

from AosCLILibrary import AosCLILibrary


class AutoChaseNe(object):
    USER = 'admin'
    PWD = 'CHGME.1a'
    FILTER_TYPE = ['fd-48e', 'fd-128', '40csm-', '96csm-']

    def __init__(self, ip, ptp):
        self.ip = ip
        self.ptp_head = ptp
        self.ptp_tail = ''
        self.fiber_map = []
        self.ptp_chain = []
        self.type = 'edge'
        self._cli = AosCLILibrary()
        print(ip)
        self._cli.cli_open_connection_and_login(ip, self.USER, self.PWD)
        print('++++++++++++++++++++++++++++++++++++++')
        print('Connected to node %s!' % ip)

    def __del__(self):
        self._cli.cli_close_connection()
        print('\nDisconnected from node %s!' % self.ip)
        print('--------------------------------------')

    def update_ptp_chain(self):
        self._update_fiber_map()
        card_head = self.ptp_head.rsplit('/', 1)[0]
        for fiber in self.fiber_map:
            if card_head in fiber:
                cards = fiber.keys()
                cards.remove(card_head)
                card_next = cards[0]
                port_next = fiber[card_next]
                card_type = self._get_card_type(card_head)
                chain_ele = {'card': card_head, 'a_end': None,
                             'z_end': fiber[card_head], 'card_type': card_type}
                self.ptp_chain.append(chain_ele)
                exit
        self._build_ptp_chain_recur(card_next, port_next)
        if not self.ptp_chain[-1]['a_end'].startswith('n'):
            self.ptp_chain[-1]['z_end'] = 'n'

    def _update_fiber_map(self):
        '''Return a fiber trace of a given ne, from the given ptp
        1. show fiber map
        admin@Atl-15> show fiber

        fiber table:

        link-name        a-end      z-end
        1/5/n:1/1/c      1/5/n      1/1/c
        1/ext-2/n:1/5/c  1/ext-2/n  1/5/c

        '''
        # return self._cli.cli_command('show fiber').cli_attrs
        fiber_map_raw = self._cli.cli_command('show fiber').cli_attrs
        for fiber_raw in fiber_map_raw:
            fiber = {}
            end_a, end_z = fiber_raw.split(':')
            c_a, p_a = end_a.rsplit('/', 1)
            c_z, p_z = end_z.rsplit('/', 1)
            fiber[c_a] = p_a
            fiber[c_z] = p_z
            self.fiber_map.append(fiber)

    def _build_ptp_chain_recur(self, card, port):
        recur = False
        chain_ele = {'card': None, 'a_end': None, 'z_end': None,
                     'card_type': None}
        for fiber in self.fiber_map:
            if card in fiber:
                chain_ele['card'] = card
                chain_ele['card_type'] = self._get_card_type(card)
                if fiber[card] == port:
                    chain_ele['a_end'] = port
                else:
                    chain_ele['z_end'] = fiber[card]
                    cards = fiber.keys()
                    cards.remove(card)
                    card_next = cards[0]
                    port_next = fiber[card_next]
                    recur = True
        self.ptp_chain.append(chain_ele)
        if recur:
            self._build_ptp_chain_recur(card_next, port_next)

    def update_ne_type(self):
        for ptp in self.ptp_chain:
            for card in ptp:
                if self._is_filter(card):
                    self.type = 'edge'
                    return
        self.type = 'transit'

    def _is_filter(self, card):
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

    def get_ptp_power(self, ptp):
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

    def is_ots(self, ptp):
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

    def get_next_node_ip(self, ptp):
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

    def get_next_node_ots(self, ptp):
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


def show_ne(ip, ptp):
    ne = AutoChaseNe(ip, ptp)
    ne.update_ptp_chain()
    # fiber_map = ne._get_fiber_map()
    # print('\nfiber map:')
    # for link_name in fiber_map:
    #     print(link_name)

    # print('\nPTP Chain:')
    # for e in ne.ptp_chain:
    #     print(e)

    # ne.update_ne_type()
    # if ne.type == 'transit':
    #     recur = True
    # print('\nNE type is: %s' % ne.type)

    for chain_ele in ne.ptp_chain:
        print('Card %s: %s' % (ptp['card'], ptp['card_type']))
        print()
        if ptp['a_end']:
            ptp = chain_ele['card'] + '/' + chain_ele['a_end']
            print('\tPort %s:' % ptp['a_end'])
            pm = ne.get_ptp_power(ptp)
            print('\t\tTx: %s' % pm[1])
            print('\t\tRx: %s' % pm[0])
        if ptp['z_end']:
            ptp = chain_ele['card'] + '/' + chain_ele['z_end']
            print('\tPort %s:' % ptp['a_end'])
            pm = ne.get_ptp_power(ptp)
            print('\t\tTx: %s' % pm[1])
            print('\t\tRx: %s' % pm[0])
    # card_type = ne._get_card_type('%s/%s' % (shelf, slot))
    # print('\nCard Type of %s/%s:' % (shelf, slot))
    # print('%s' % card_type)

    # pm = ne._get_ptp_power(ptp)
    # print('\nPM readings of %s:' % ptp)
    # print('pm_r: %s' % pm[0])
    # print('pm_t: %s' % pm[1])

    # print('\nIs %s with ots?' % ptp)
    # print(ne._is_ots(ptp))
    # print('Is %s with ots?' % '1/5/n')
    # print(ne._is_ots('1/5/n'))

    next_ne = {'ip': None, 'ptp': None}
    ptp_tail_card = ne.ptp_chain[-1].keys()[0]
    ptp_tail_port = ne.ptp_chain[-1][ptp_tail_card]['z_end']
    ptp_tail = ptp_tail_card + '/' + ptp_tail_port
    if ne.is_ots(ptp_tail):
        next_ne['ip'] = ne.get_next_node_ip(ptp_tail)
        next_ne['ptp'] = ne.get_next_node_ots(ptp_tail)
    return next_ne


NE15 = {
    'ip': '10.16.45.15',
    'shelf': '1',
    'slot': 'ext-2',
    'port': 'n'
}

NE14 = {
    'ip': '10.16.45.14',
    'shelf': '1',
    'slot': '2',
    'port': 'n'
}

NE13 = {
    'ip': '10.16.45.13',
    'shelf': '1',
    'slot': '2',
    'port': 'n'
}

NE11 = {
    'ip': '10.16.45.11',
    'shelf': '1',
    'slot': 'ext-1',
    'port': 'n'
}

NE12 = {
    'ip': '10.16.45.12',
    'shelf': '1',
    'slot': '2',
    'port': 'n'
}


def test():
    nes = [NE14]
    for ne in nes:
        show_ne(ne['ip'], ne['shelf'], ne['slot'])


if __name__ == '__main__':
    ne = NE15
    ip = ne['ip']
    shelf = ne['shelf']
    slot = ne['slot']
    port = ne['port']
    ptp = '%s/%s/%s' % (shelf, slot, port)
    next_ne = show_ne(ip, ptp)
    while next_ne['ip']:
        next_ne = show_ne(next_ne['ip'], next_ne['ptp'])
