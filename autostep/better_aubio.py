from subprocess import check_output

def tempo(song_filename: str) -> int:
	return int(float(check_output(f"aubio tempo {song_filename}", shell=True, text=True).replace(" bpm", "")))

def onset(song_filename: str) -> tuple[float, ...]:
	return tuple(float(timestamp) for timestamp in check_output(f"aubio onset {song_filename}", shell=True, text=True).splitlines())
