'''
Created on 15.12.2013

@author: lony

http://stackoverflow.com/questions/11515944/how-to-use-multiprocessing-queue-in-python
http://stackoverflow.com/questions/13941562/why-can-i-not-catch-a-queue-empty-exception-from-a-multiprocessing-queue
http://stackoverflow.com/questions/11996632/multiprocessing-in-python-while-limiting-the-number-of-running-processes
'''

import subprocess, os, sys, time, multiprocessing, Queue, itertools

wordlist = [
"foo",
"bar",
"zoo",
"hello",
"World",
]
tcFile = r"C:\dev\tc-brute-force\test.pa"
tcProg = r"C:\Program Files\TrueCrypt\TrueCrypt.exe"
tcMountLetter = "z"
verbose = 4 # as higher as more output is shown fatal=0-5=trace
counter = 0
numberofworkers = multiprocessing.cpu_count()*2
curenttime = time.time()

def getDuration(starttime):
		return time.time() - starttime

def callTC(password, event):
	commandArgs = [
		tcProg,
		'/a',
		'/s',
		'/q',
		'/v', tcFile,
		'/l', tcMountLetter,
		'/p',  password,
	]
		
	child = subprocess.Popen(commandArgs, \
		stderr=open(os.devnull, 'w'), \
		stdout=open(os.devnull, 'w'))
	result = child.communicate() # Really important to get error code!
		
	if verbose > 4:
		print subprocess.list2cmdline(commandArgs).rstrip() + \
			" Status out=" + str(result[0]) + \
			" err=" + str(result[1]) + \
			", code=" + str(child.returncode)

	if child.returncode == 0:
		event.set()
		print "Successfully opened TrueCrypt file with '%s' at iteration %d, duration %.3fs" % (password, counter, getDuration(curenttime))
		
def callTCDaemon(queue, event):
	while True:
		if queue.empty():
			break
		else:
			password = queue.get()
			callTC(password, event)

if __name__ == '__main__':

	manager = multiprocessing.Manager()
	event = manager.Event()
	worker = manager.Queue(numberofworkers)

	# start processes
	pool = []
	for i in xrange(numberofworkers):
		process = multiprocessing.Process(target=callTCDaemon, args=(worker, event))
		process.start()
		pool.append(process)

	# generate permutations
	for x in xrange(1, (len(wordlist)+1) ):
		for permutation in itertools.permutations(wordlist, x):
			
			# shutdown if result is found
			if event.is_set():
				# wait till finished
				for p in pool:
					p.join(2)
			
				print "Finished TrueCrypt brute-force, after %d attempts, duration %.3fs" % (counter, getDuration(curenttime))
				sys.exit(1)

			counter += 1	
			combination = ""

			# build string from permutation
			for i in range(0, len(permutation)):
				combination += permutation[i]

			# output progress
			if verbose == 4 and counter%100 == 0:
				print "%15d|%15.3fs: %s" % (counter, getDuration(curenttime), combination)

			# avoid queue overload
			while worker.qsize() > 100:
				if verbose > 3:	print "Wait because queue is full, size=%d" % (worker.qsize)
				time.sleep(4)			
			
			worker.put(combination)