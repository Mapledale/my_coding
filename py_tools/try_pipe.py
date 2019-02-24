#! /usr/bin/env python

import os
from subprocess import Popen, PIPE
import time

def pipe2xterm(pipe_id, content):
	from subprocess import Popen, PIPE
	import os
	
	if not os.path.exists(pipe_id):
		os.mkfifo(pipe_id)
	
	#Popen(['x-terminal-emulator', '-e', 'tail -f %s' %pipe_id])
	with open(pipe_id, 'w') as p:
		p.write(content)
	
for i in range(5):
	print('line in main terminal: %d' %i)
	
for n in range(3):
	pipe_path = 'my_pipe' + str(n)
	
	if not os.path.exists(pipe_path):
		os.mkfifo(pipe_path)
	
	Popen(['x-terminal-emulator', '-e', 'tail -f %s' %pipe_path])
	
	for _ in range(5):
		pipe2xterm(pipe_path, 'line in xterm: %d\r' %_)
		time.sleep(1)

print('--------------')
for i in range(5):	
	print('line in main terminal: %d' %(i + 5))
	
