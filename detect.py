from Song import *
from scipy import signal
import librosa
import aubio
from typing import Optional

# Detection functions take the song as the first parameter
# and all parameters after must be integers
# And must return a ndarray of samples

# Performance not that good
def scipyPeaks(
	song: Song,
	threshold: Optional[int] = None,
	distance: Optional[int] = None
) -> np.ndarray:
	return signal.find_peaks(song.data, threshold = threshold, distance = distance)[0]

# Will basically generate no 16th notes
# Irredeemable
def librosaPeaks(song: Song, tightness: int = 100, 
		hop_length: int = 512, trim: bool = True) -> np.ndarray:
	return librosa.beat.beat_track(song.data, hop_length = hop_length,
		tightness = tightness, trim = trim, sr = song.samplerate, 
		bpm = song.bpm, units = 'samples')[1]

# Similar to scipy, performance not that good
def aubioPeaks(song: Song, fft: int, hop: int, mode: int) -> np.ndarray:
	if mode <= 0 or mode > 8:
		algorithm = 'default'
	else:
		algorithm = {
			1: 'complex',
			2: 'energy',
			3: 'phase',
			4: 'specdiff',
			5: 'specflux',
			6: 'kl',
			7: 'mkl',
			8: 'hfc'
		}[mode]
	
	# We can't use the existing song data for this
	s = aubio.source(song.filepath, song.samplerate, hop)
	o = aubio.onset(algorithm, fft, hop, song.samplerate)
	
	onsets = []
	num_read = hop
	while num_read >= hop:
		samples, num_read = s()
		if o(samples):
			onsets.append(o.get_last())

	return np.int32(onsets)

def overThresholdPeaks(song: Song, threshold: int) -> np.ndarray:
	return np.where(song.data > threshold)[0]

