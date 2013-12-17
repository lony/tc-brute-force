'''
Created on 15.12.2013

@author: lony
'''

import itertools, mmap

wordlist = [
"foo",
"bar",
"zoo",
]

# open files
fileIn = open("InPasswordPermutations.txt", "r")
fileInMap = mmap.mmap(fileIn.fileno(), 0, access=mmap.ACCESS_READ)
fileOut = open("OutPasswordPermutations.txt", "w")


# create list of permutations and run over all permutations
for x in xrange(1, (len(wordlist)+1) ):
	for permutation in itertools.permutations(wordlist, x):
		combination = ""
 
		# concatenate permutation to a string
		for i in xrange(0, len(permutation)):
			combination += permutation[i]
		#print combination

		# search if string is already tested
		# else: store string    
		if fileInMap.find(combination) is -1:
			print>>fileOut, combination
		#else:
		#    print combination

fileIn.close	
fileOut.close