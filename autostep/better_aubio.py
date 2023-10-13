from subprocess import check_output
from typing import Literal

def tempo(song_filename: str) -> int:
	return int(float(check_output(f"aubio tempo {song_filename}", shell=True, text=True).replace(" bpm", "")))

OnsetMethod = Literal['default', 'energy', 'hfc', 'complex', 'phase', 'specdiff', 'kl', 'mkl', 'specflux']

def onset(song_filename: str, method: OnsetMethod) -> tuple[float, ...]:
	return tuple(float(timestamp) for timestamp in check_output(f"aubio onset -m {method} {song_filename}", shell=True, text=True).splitlines())
