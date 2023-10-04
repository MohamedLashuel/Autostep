from numpy import \
	float32 as np_float32, \
	int16 as np_int16
from numpy.typing import NDArray
from scipy.io import wavfile
from scipy import signal
from sounddevice import \
	play as sd_play, \
	stop as sd_stop

class Waveform:
	@staticmethod
	def from_file(filename: str) -> 'Waveform':
		return Waveform(*wavfile.read(filename))

	def __init__(self, sample_rate: int, data: NDArray[np_float32]):
		self.sample_rate, self.data = sample_rate, data
		self.nyquist_freq = 0.5 * self.sample_rate
	
	def __getitem__(self, key):
		if isinstance(key, slice):
			return Waveform(self.sample_rate, self.data[key.start : key.stop : key.step])
		elif isinstance(key, int):
			return self.data[key]

	def slice_seconds(self, begin: int, end: int) -> 'Waveform':
		return Waveform(self.sample_rate, self.data[begin * self.sample_rate : end * self.sample_rate])
	
	def lowpass(self, cutoff_freq_hz: int, order: int) -> 'Waveform':
		b, a = signal.butter(order, freq / self.nyquist_freq, btype='lowpass')
		return Waveform(self.sample_rate, signal.filtfilt(b, a, self.data, axis=0))
	
	def bandpass(self, f1_hz: int, f2_hz: int, order: int) -> 'Waveform':
		band = (f1_hz / self.nyquist_freq, f2_hz / self.nyquist_freq)
		b, a = signal.butter(order, band, btype='bandpass')
		return Waveform(self.sample_rate, signal.filtfilt(b, a, self.data, axis=0))
	
	def highpass(self, cutoff_freq_hz: int, order: int) -> 'Waveform':
		b, a = signal.butter(order, cutoff_freq_hz / self.nyquist_freq, btype='highpass')
		return Waveform(self.sample_rate, signal.filtfilt(b, a, self.data, axis=0))

	def save_to_file(self, filename: str) -> None:
		wavfile.write(filename, self.sample_rate, np_int16(self.data))

	def play(self) -> None:
		sd_play(self.data, self.sample_rate)

	def stop(self) -> None:
		sd_stop()
