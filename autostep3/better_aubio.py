from typing import Callable, Literal
from autostep3.util import NDFloatArray, NDIntArray
import numpy as np
import aubio
import subprocess
import math

shell_exec: Callable[[str], str]
shell_exec = lambda command: subprocess.check_output(command, shell=True, text=True)

tempo_cli: Callable[[str], float]
tempo_cli = lambda filename: float(shell_exec(f"aubio tempo {filename}").replace(" bpm", ""))

OnsetMethod = Literal['default', 'energy', 'hfc', 'complex', 'phase', 'specdiff', 'kl', 'mkl', 'specflux']

# Returns onsets in SECONDS
onset_cli: Callable[[str, OnsetMethod], NDFloatArray]
onset_cli = lambda filename, method = "default": np.array([s for s in shell_exec(f"aubio onset {filename} -m {method}").splitlines()], dtype=np.float_)

# https://github.com/aubio/aubio/blob/master/python/demos/demo_onset.py
# Returns onsets in SAMPLES
def onset(filename: str, method: OnsetMethod = "default") -> NDIntArray:
	s = aubio.source(filename) # type: ignore
	o = aubio.onset(method) # type: ignore
	onsets: list[int] = []
	read = math.inf
	while read > 0:
		samples, read = s()
		if o(samples):
			onsets.append(o.get_last())
	return np.array(onsets)
