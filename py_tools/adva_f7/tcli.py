#! /usr/bin/env python2

import time
from TCLILibrary import tcliclient

ip = '10.16.24.30'
alias1 = 'conn1'
shelf = '11'
slot = '5'
chan = '19500'
port_c = 'C2'
vch_from = 'VCH-' + shelf + '-' + slot + '-N-' + chan
vch_to = 'VCH-' + shelf + '-' + slot + '-' + port_c + '-' + chan
aid_f = vch_from + ',' + vch_to
crs_create_f = 'CRSCREATE::' + aid_f + ':PATH-NODE=1;'
crs_destroy_f = 'CRSDESTROY::' + aid_f + ';'

def create(alias, cmd):
	my_conn = tcliclient.TCLIclient()
	my_conn.open_connection(ip, alias)	
	cmd_rst = my_conn.write(cmd)
	print(alias + ':\n' + cmd_rst	
	n = tcliclient.TCLIclient()
	
	
def crs_test(alias):
	tcli = tcliclient.TCLIclient()
	tcli.open_connection(ip, alias)
	
	crs_f = tcli.write(crs_create_f)
	print(alias + ': CRS created')
	time.sleep(5)
	#crs_f = tcli.write(crs_create_f)
	#print(alias + ': CRS creation failed')
	
	crs_f = tcli.write(crs_destroy_f)
	print(alias + ': CRS deleted\n')
	
	tcli.close_connection(alias)

if __name__ == '__main__':
	sess = 'conn1'
	cmd_create_om-n = 'CREATE::OM-' + shelf '-' + slot + '-N;'
	# crs_test(id)
	create(sess, cmd_create_om-n)
