'''
Created on 15.12.2013

@author: lony
'''

import itertools

wordlist = [
"foo",
"bar",
"zoo",
]

f = open("OutPasswordPermutations.txt", "w")

for x in xrange(1, (len(wordlist)+1) ):
	for permutation in itertools.permutations(wordlist, x):
		combination = ""
 
		# concatenate permutation to a string
		for i in xrange(0, len(permutation)):
			combination += permutation[i]
		# print combination
		print>>f, combination

f.close