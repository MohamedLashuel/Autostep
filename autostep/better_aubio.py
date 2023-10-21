from subprocess import check_output
from typing import Literal, Optional
from math import inf
import numpy as np
import aubio

def shell_exec(command: str) -> str:
	return check_output(command, shell=True, text=True)

def tempo(song_filename: str) -> int:
	return int(float(shell_exec(f"aubio tempo {song_filename}").replace(" bpm", "")))

OnsetMethod = Literal['default', 'energy', 'hfc', 'complex', 'phase', 'specdiff', 'kl', 'mkl', 'specflux']

def onset_seconds(song_filename: str, method: OnsetMethod) -> tuple[float, ...]:
	return tuple(float(timestamp) for timestamp in shell_exec(f"aubio onset -m {method} {song_filename}").splitlines())

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

def quiet(song_filename: str, silence_threshold: Optional[int] = None) -> tuple[float, ...]:
	"""
	NOTE: In the returned tuple, even indices are `NOISY`, and odd indices are `QUIET`
	"""
	if silence_threshold is None:
		output = shell_exec(f"aubio quiet {song_filename}")
	else:
		output = shell_exec(f"aubio quiet {song_filename} -s {silence_threshold}")
	timestamps = []
	for line in output.splitlines():
		timestamps.append(float(line.replace("NOISY: ", "").replace("QUIET: ", "")))
	return tuple(timestamps)
