from array2chart import *
from itertools import product
from typing import Callable
from numpy import ndarray

def readCodeTxt(filename = 'code.txt') -> str:
	with open(filename) as f:
		return f.read()

def runTest(song: Song, peaks: ndarray, grade_func: Callable[[str], int], *params, print_params = False):
	arrayToChart(peaks, song)
	# Print with tab to make grade results visible
	if print_params: print(f'\t{params}')
	return grade_func(readCodeTxt())
	
# param_values is a tuple of iterables containing the values every parameter
# can take when calling detect_func

# Return the set of parameters that yields the lowest score (lower = better)

def optimize(song: Song, grade_func: Callable, detect_func: Callable, *args):
	for tup in args:
		assert len(tup)
	min_score = None
	min_combo = None
	for combo in product(*args):
		peaks = detect_func(song, *combo)
		score = runTest(song, peaks, grade_func, combo, print_params = True)
		if min_score is None or score < min_score:
			min_score = score
			min_combo = combo
	return min_combo

# Tests take in one parameter, the code to be analyzed
def thirtysecondtest(code):
	sixteenths = 0
	thirtyseconds = 0
	on_sixteenth = True
	for chr in code:
		if chr == '/':
			continue
		elif chr == 'n':
			if on_sixteenth:
				sixteenths += 1
			else:
				thirtyseconds += 1
		on_sixteenth = not on_sixteenth
	print(f'Sixteenths: {sixteenths}')
	print(f'Thirtyseconds: {thirtyseconds}')
	return thirtyseconds
