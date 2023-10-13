from subprocess import check_output

def aubio_tempo(song_filename: str):
	return int(float(check_output(f"aubio tempo {song_filename}", shell=True, text=True).replace(" bpm", "")))