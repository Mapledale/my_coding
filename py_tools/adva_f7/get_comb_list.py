#! /usr/bin/env python2
'''
Generate a text file listing all the channels with a good comb signal.
For OPR type:
read OPR on VCH-N for every channels and count those with OPR higher than a threshold as Hot channels
For OPT type:
Suppose the comb signal is fed to a client port of a ROADM (OM-shelf-slot-Ci) at an NE.
That ROADM has adding CRS InService on all 96 channels from that client port to network port.
Then read OPT on VCH-N for every channels and count those channels with OPT higher than a threshold as Hot channels.
Results are written to a text file.
'''
import sys
import re
from time import sleep
from TCLILibrary import tcliclient

def main():
    ip = raw_input('Please input the ip address of the ROADM node: ')
    shelf = raw_input('Please input the shelf # of the ROADM: ')
    slot = raw_input('Please input the slot # of the ROADM: ')
    pm_id = raw_input('Please input the PM type - 1 for OPT, 2 for OPR: ')
    
    if pm_id == '1':
        pm_type = 'OPT'
    elif pm_id == '2':
        pm_type = 'OPR'
    alias = 'comb'
    chan_all = range(19600, 19120, -5)
    thrLow = -50    # pm reading less than thrLow will be treated as n/a
    chan_comb = []
    aid_om_n = 'OM-' + shelf + '-' + slot + '-N'
    cmd_pmupdate = 'SET::' + aid_om_n + ':OPR_PMUPDATE=OPR;'
    cmd_eqlz = 'SET::' + aid_om_n + ':OPR-EQLZ=OPR;'
    re_patt_pm = re.compile(r'OP[TR]: [-0-9.]+', re.DOTALL)
    filename = 'comb_list.txt'
        
    tcli = tcliclient.TCLIclient()
    tcli.open_connection(ip, alias)
    print('\nConnected to NE ' + ip)
    
    if pm_id == '1':
        tcli.write_dont_care(cmd_eqlz)
        sleep(60)
    
    print('Strart to read PM of each channel...')
    for i in chan_all:
        aid_vch_n = 'VCH-' + shelf + '-' + slot + '-N-' + str(i)
        if pm_id == '2':
            tcli.write_dont_care(cmd_pmupdate)
            sleep(1)
        cmd_get_pm = 'GET::' + aid_vch_n + ':' + pm_type + ';'        
        
        rst_get_pm = tcli.write_dont_care(cmd_get_pm)
        # the first write_dont_care doesn't refresh the result
        rst_get_pm = tcli.write_dont_care(cmd_get_pm)
        
        pm = re_patt_pm.search(rst_get_pm)
        pm = pm.group(0)
        pm = pm.lstrip(pm_type + ': ')
        
        if float(pm) < thrLow:
            pm = 'n/a  '
        else:
            chan_comb.append(str(i) + ': ' + pm)
        
        sys.stdout.write('\r')
        sys.stdout.write('Reading on channel ' + str(i) + ': ' + pm)
        sys.stdout.flush()
        
    print('\nFinished reading PM.')        
    tcli.close_connection(alias)
    print('Connection to ' + ip + ' closed.\n')
    
    print('Writing all readings to file ' + filename + ' ...\n')
    num_hot_ch = len(chan_comb)
    file_comb = open(filename, 'w')
    file_comb.write('Total %s Hot Channels for %s:\n' %(str(num_hot_ch), pm_type)) 
    for line in chan_comb:
        file_comb.write(line + '\n')
    file_comb.write('The End\n')
    file_comb.close()
    print('Done!')

if __name__ == '__main__':
    main()
