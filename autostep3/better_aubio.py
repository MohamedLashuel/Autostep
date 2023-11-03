from typing import Callable, Literal
from util import NDIntArray
import numpy as np
import aubio
import subprocess
import math

shell_exec: Callable[[str], str]
shell_exec = lambda command: subprocess.check_output(command, shell=True, text=True)

tempo_cli: Callable[[str], float]
tempo_cli = lambda filename: int(float(shell_exec(f"aubio tempo {filename}").replace(" bpm", "")))

OnsetMethod = Literal['default', 'energy', 'hfc', 'complex', 'phase', 'specdiff', 'kl', 'mkl', 'specflux']

# https://github.com/aubio/aubio/blob/master/python/demos/demo_onset.py
# Returns onsets in SAMPLES
def onset(
	filename: str,
	method: OnsetMethod = "complex",
	*,
	fft_size: int = 1024,
	hop_size: int = 512
) -> NDIntArray:
	s = aubio.source(filename) # type: ignore
	o = aubio.onset(method, fft_size, hop_size) # type: ignore
	onsets: list[int] = []
	read = math.inf
	while read > 0:
		samples, read = s()
		if o(samples):
			onsets.append(o.get_last())
	return np.array(onsets)
