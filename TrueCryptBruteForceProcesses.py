'''
Created on 15.12.2013

@author: lony

https://code.google.com/p/truecrack/
https://code.google.com/p/tckeyfilehack
https://code.google.com/p/tcdiscover/
http://blog.bjrn.se/2008/01/truecrypt-explained.html
http://stackoverflow.com/questions/11515944/how-to-use-multiprocessing-queue-in-python
http://stackoverflow.com/questions/13941562/why-can-i-not-catch-a-queue-empty-exception-from-a-multiprocessing-queue
http://stackoverflow.com/questions/11996632/multiprocessing-in-python-while-limiting-the-number-of-running-processes
http://stackoverflow.com/questions/20627714/python-multiprocessing-with-subprocess-stops-working
'''

import itertools, sys, os, time, multiprocessing
from subprocess import Popen
from multiprocessing.dummy import Pool  # use threads

word_list = [
"foo",
"bar",
"zoo",
"hello",
"World",
]
tc_file = r"C:\dev\tc-brute-force\test.pa"
tc_prog = r"C:\Program Files\TrueCrypt\TrueCrypt.exe"
tc_mount_letter = "x"
verbose = 1
number_of_workers = multiprocessing.cpu_count() * 10
curent_time = time.time()

def get_duration(starttime):
	return time.time() - starttime

def generate_passwords(wordlist):
	for password_length in xrange(1, len(wordlist) + 1):  # no repeats
		for password in itertools.permutations(wordlist, password_length):
				yield "".join(password)

def valid_password(password):
	command_args = [
		tc_prog,
		'/a',
		'/s',
		'/q',
		'/v', tc_file,
		'/l', tc_mount_letter,
		'/p', password,
	]	
	child = Popen(command_args, close_fds=True)
	result = child.communicate() # Really important to get error code!
	sys.stderr.write("rc==%s\n" % child.returncode)
	
	if child.returncode == 0:
		sys.stderr.write("Successfully opened TrueCrypt file with '%s', duration %.3fs\n" % (password, get_duration(curent_time)))
    	return True, password

if __name__ == '__main__':
	pool = Pool(number_of_workers)
	for i, (found, password) in enumerate(pool.imap(valid_password, generate_passwords(word_list))):
    	 if i % 1000 == 0 or verbose == 1:  # report progress
    	     sys.stderr.write("%15d|%15.2fs: %s\n" % (i, get_duration(curent_time), password))
    	 if found:
    		 break
	else:
  		sys.exit("Finished TrueCrypt brute-force, after %d attempts, duration %.3fs" % (i, get_duration(curent_time)))

	#pool.close() 
	#pool.join() # uncomment if it is not the end
