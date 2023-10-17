import numpy as np
import sounddevice as sd
from numpy.typing import NDArray
from scipy.io import wavfile
from scipy import signal

class Waveform:
	@staticmethod
	def from_file(filename: str) -> 'Waveform':
		return Waveform(*wavfile.read(filename))

	def __init__(self, samplerate: int, data: NDArray[np.float32]):
		self.samplerate, self.data = samplerate, data
		self.nyquist_freq = 0.5 * self.samplerate
	
	def __getitem__(self, key):
		if isinstance(key, slice):
			return Waveform(self.samplerate, self.data[key.start : key.stop : key.step])
		elif isinstance(key, int):
			return self.data[key]

	def slice_seconds(self, begin: int, end: int) -> 'Waveform':
		return Waveform(self.samplerate, self.data[begin * self.samplerate : end * self.samplerate])
	
	def lowpass(self, cutoff_freq_hz: int, order: int) -> 'Waveform':
		b, a = signal.butter(order, cutoff_freq_hz / self.nyquist_freq, btype='lowpass')
		return Waveform(self.samplerate, signal.filtfilt(b, a, self.data, axis=0))
	
	def bandpass(self, f1_hz: int, f2_hz: int, order: int) -> 'Waveform':
		band = (f1_hz / self.nyquist_freq, f2_hz / self.nyquist_freq)
		b, a = signal.butter(order, band, btype='bandpass')
		return Waveform(self.samplerate, signal.filtfilt(b, a, self.data, axis=0))
	
	def highpass(self, cutoff_freq_hz: int, order: int) -> 'Waveform':
		b, a = signal.butter(order, cutoff_freq_hz / self.nyquist_freq, btype='highpass')
		return Waveform(self.samplerate, signal.filtfilt(b, a, self.data, axis=0))

	def save_to_file(self, filename: str) -> None:
		wavfile.write(filename, self.samplerate, np.int16(self.data))

	def play(self) -> None:
		sd.play(self.data, self.samplerate)

	def stop(self) -> None:
		sd.stop()
