from typing import Callable, Literal
try:
	from util import NDIntArray
except ModuleNotFoundError:
	from autostep3.util import NDIntArray
import numpy as np
import aubio
import subprocess
import math

shell_exec: Callable[[str], str]
shell_exec = lambda command: subprocess.check_output(command, shell=True, text=True)

tempo_cli: Callable[[str], float]
tempo_cli = lambda filename: int(float(shell_exec(f"aubio tempo {filename}").replace(" bpm", "")))

ONSET_METHODS = "default", "energy", "hfc", "complex", "phase", "specdiff", "kl", "mkl", "specflux"
OnsetMethod = Literal["default", "energy", "hfc", "complex", "phase", "specdiff", "kl", "mkl", "specflux"]

# https://github.com/aubio/aubio/blob/master/python/demos/demo_onset.py
def onset(
	filename: str,
	method: OnsetMethod,
	*,
	fft_size: int = 1024,
	hop_size: int = 512
) -> NDIntArray:
	if method not in ONSET_METHODS:
		raise ValueError("`method` is not a valid onset method")
	s = aubio.source(filename) # type: ignore
	o = aubio.onset(method, fft_size, hop_size) # type: ignore
	onsets: list[int] = []
	read = math.inf
	while read > 0:
		samples, read = s()
		if o(samples):
			onsets.append(o.get_last())
	return np.array(onsets)
