'''
Created on 15.12.2013

@author: lony
'''

import subprocess, os, sys, time, itertools

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
curenttime = time.time()

def getDuration(starttime):
		return time.time() - starttime

def callTC(password):
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
		print "Successfully opened TrueCrypt file with '%s' at iteration %d, duration %.3fs" % (password, counter, getDuration(curenttime))
		return True
	else:
		return False

if __name__ == '__main__':

	# generate permutations
	for x in xrange(1, (len(wordlist)+1) ):
		for permutation in itertools.permutations(wordlist, x):		
			counter += 1	
			combination = ""

			# build string from permutation
			for i in range(0, len(permutation)):
				combination += permutation[i]

			# output progress
			if verbose == 4 and counter%100 == 0:
				print "%15d|%15.3fs: %s" % (counter, getDuration(curenttime), combination)

			if callTC(combination):
				sys.exit(0)

	print "Finished TrueCrypt brute-force, after %d attempts, duration %.3fs" % (counter, getDuration(curenttime))
	sys.exit(1)