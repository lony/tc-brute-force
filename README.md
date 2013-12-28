tc-brute-force
==============

Python script to brute force TrueCrypt passwords on Windows using TC command line api

# ToDo, for TrueCryptBruteForce.py
- Calculate permutations before starting calculation n!/(n-k)! ; n=element count; k=draws
- Progressbar
- Calculating permutations based on (simple) RegEx
	https://code.google.com/p/xeger/
	http://stackoverflow.com/questions/1667528/regular-expression-listing-all-possibilities
	http://stackoverflow.com/questions/1248519/how-can-i-expand-a-finite-pattern-into-all-its-possible-matches
- Make multiprocessing work, see TrueCryptBruteForceProcesses.py
