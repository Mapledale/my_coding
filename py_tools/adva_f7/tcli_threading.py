#! /usr/bin/env python2

import threading
import time
from TCLILibrary import tcliclient

ip = '10.16.24.30'
alias = 'conn'
shelf = '11'
slot = '5'
chan = '19500'
port_c = 'C2'
vch_from = 'VCH-' + shelf + '-' + slot + '-N-' + chan
vch_to = 'VCH-' + shelf + '-' + slot + '-' + port_c + '-' + chan
aid_f = vch_from + ',' + vch_to
crs_create_f = 'CRSCREATE::' + aid_f + ':PATH-NODE=1;'
crs_destroy_f = 'CRSDESTROY::' + aid_f + ';'

class crs_test(threading.Thread):
	def __init__(self, alias):
		threading.Thread.__init__(self)
		self.alias = alias
		
	def run(self):
		tcli = tcliclient.TCLIclient()
		tcli.open_connection(ip, self.alias)
	
		crs_f = tcli.write_dont_care(crs_create_f)
		print(self.alias + ': CRS created')
		time.sleep(6)
		
		crs_f = tcli.write_dont_care(crs_destroy_f)
		print(self.alias + ': CRS deleted\n')
	
		tcli.close_connection(self.alias)
		
def main():
	test_rst = []
	
	for i in range(30):
		alias_i = alias + str(i)
		test_current = crs_test(alias_i)
		test_rst.append(test_current)
		test_current.start()
	
	for t in test_rst:
		t.join()
		print('done')

if __name__ == '__main__':
	main()
