'''
Created on 15.12.2013

@author: lony

http://stackoverflow.com/questions/11515944/how-to-use-multiprocessing-queue-in-python
http://stackoverflow.com/questions/13941562/why-can-i-not-catch-a-queue-empty-exception-from-a-multiprocessing-queue
http://stackoverflow.com/questions/11996632/multiprocessing-in-python-while-limiting-the-number-of-running-processes
http://stackoverflow.com/questions/20627714/python-multiprocessing-with-subprocess-stops-working
'''

import subprocess, os, sys, time, multiprocessing, Queue, itertools

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
verbose = 4 # as higher as more output is shown fatal=0-5=trace
counter = 0
number_of_workers = multiprocessing.cpu_count()*2
curent_time = time.time()

def get_duration(starttime):
		return time.time() - starttime

def call_tc(password, event):
	command_args = [
		tc_prog,
		'/a',
		'/s',
		'/q',
		'/v', tc_file,
		'/l', tc_mount_letter,
		'/p',  password,
	]
		
	child = subprocess.Popen(command_args, \
		stderr=open(os.devnull, 'w'), \
		stdout=open(os.devnull, 'w'))
	result = child.communicate() # Really important to get error code!
		
	if verbose > 4:
		print subprocess.list2cmdline(command_args).rstrip() + \
			" Status out=" + str(result[0]) + \
			" err=" + str(result[1]) + \
			", code=" + str(child.returncode)

	if child.returncode == 0:
		event.set()
		print "Successfully opened TrueCrypt file with '%s' at iteration %d, duration %.3fs" % (password, counter, get_duration(curent_time))
		
def call_tc_daemon(queue, event):
	while True:
		if queue.empty():
			break
		else:
			password = queue.get()
			call_tc(password, event)

if __name__ == '__main__':

	manager = multiprocessing.Manager()
	event = manager.Event()
	worker = manager.Queue(number_of_workers)

	# start processes
	pool = []
	for i in xrange(number_of_workers):
		process = multiprocessing.Process(target=call_tc_daemon, args=(worker, event))
		process.start()
		pool.append(process)

	# generate permutations
	for x in xrange(1, (len(word_list)+1) ):
		for permutation in itertools.permutations(word_list, x):
			
			# shutdown if result is found
			if event.is_set():
				# wait till finished
				for p in pool:
					p.join(2)
			
				print "Finished TrueCrypt brute-force, after %d attempts, duration %.3fs" % (counter, get_duration(curent_time))
				sys.exit(1)

			counter += 1	
			combination = ""

			# build string from permutation
			for i in range(0, len(permutation)):
				combination += permutation[i]

			# output progress
			if verbose == 4 and counter%100 == 0:
				print "%15d|%15.3fs: %s" % (counter, get_duration(curent_time), combination)

			# avoid queue overload
			while worker.qsize() > 100:
				if verbose > 3:	print "Wait because queue is full, size=%d" % (worker.qsize)
				time.sleep(4)			
			
			worker.put(combination)