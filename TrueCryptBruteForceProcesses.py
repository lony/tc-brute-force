'''
Created on 15.12.2013

@author: lony

http://stackoverflow.com/questions/11515944/how-to-use-multiprocessing-queue-in-python
http://stackoverflow.com/questions/13941562/why-can-i-not-catch-a-queue-empty-exception-from-a-multiprocessing-queue
http://stackoverflow.com/questions/11996632/multiprocessing-in-python-while-limiting-the-number-of-running-processes
http://stackoverflow.com/questions/20627714/python-multiprocessing-with-subprocess-stops-working
'''

import itertools, sys, time, multiprocessing
from subprocess import call
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
tc_mount_letter = "z"
verbose = 1
number_of_workers = multiprocessing.cpu_count() * 10
curent_time = time.time()

def get_duration(starttime):
	return time.time() - starttime

def generate_passwords(wordlist):
	for password_length in range(1, len(wordlist) + 1):  # no repeats
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
	rc = call(command_args, close_fds=True)
    	return rc == 0, password

if __name__ == '__main__':

	pool = Pool(number_of_workers)
	for i, (found, password) in enumerate(pool.imap_unordered(valid_password, generate_passwords(word_list))):
    	 if i % 1000 == 0 or verbose == 1:  # report progress
    	     sys.stderr.write("%15d|%15.2fs: %s\n" % (i, get_duration(curent_time), password))
    	 if found:
    		 print ("Successfully opened TrueCrypt file with '%s' at iteration %d, duration %.3fs" % (password, i, get_duration(curent_time)))
    		 break
	else:
  		sys.exit("Finished TrueCrypt brute-force, after %d attempts, duration %.3fs" % (i, get_duration(curent_time)))

	pool.close() 
	#pool.join() # uncomment if it is not the end
