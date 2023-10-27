from subprocess import check_output
from typing import Literal
from math import inf
import aubio

def shell_exec(command: str) -> str:
	return check_output(command, shell=True, text=True)

def tempo(song_filename: str) -> int:
	return int(float(shell_exec(f"aubio tempo {song_filename}").replace(" bpm", "")))

OnsetMethod = Literal['default', 'energy', 'hfc', 'complex', 'phase', 'specdiff', 'kl', 'mkl', 'specflux']

def onset_samples(filename: str, method: OnsetMethod) -> list[int]:
	s = aubio.source(filename)
	o = aubio.onset(method)
	onsets = []
	read = inf
	while read > 0:
		samples, read = s()
		if o(samples):
			onsets.append(o.get_last())
	return onsets
