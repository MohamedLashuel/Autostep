from obj import *
from scipy import signal
import librosa
import aubio

# Detection functions take the song as the first parameter
# and all parameters after must be integers
# And must return a ndarray of samples

# Performance not that good
def scipyPeaks(song: Song, threshold: int = None,
	 distance: int = None) -> np.ndarray:
	return signal.find_peaks(song.data, 
		threshold = threshold, distance = distance)[0]

# Will basically only generate 16th notes, not 4th or 8th.
# Irredeemable
def librosaPeaks(song: Song, tightness: int = 100, 
		hop_length: int = 512, trim: bool = True) -> np.ndarray:
	return librosa.beat.beat_track(song.data, hop_length = hop_length,
		tightness = tightness, trim = trim, sr = song.samplerate, 
		bpm = song.bpm, units = 'samples')[1]

def aubioPeaks(song: Song, fft: int, hop: int) -> np.ndarray:
	# We can't use the existing song data for this
	s = aubio.source(song.filepath, song.samplerate, hop)
	o = aubio.onset('default', fft, hop, song.samplerate)
	
	onsets = []
	num_read = hop
	while num_read >= hop:
		samples, num_read = s()
		if o(samples): onsets.append(o.get_last())

	return np.int32(onsets)