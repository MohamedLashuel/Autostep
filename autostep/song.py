import numpy as np
from scipy.io import wavfile
from scipy import signal
from typing import Literal

class Song:
	def __init__(self, filepath: str, bpm: float, offset: float):
		self.samplerate, self.data = wavfile.read(filepath)
		self.nyquist_freq = self.samplerate * 0.5
		self.filepath = filepath
		self.data = average_channels(self.data)
		self.bpm = bpm
		self.offset = offset

	def save_to_file(self, filename: str) -> None:
		# Convert to integer for PCM format. HAS TO BE int16
		wavfile.write(filename, self.samplerate, np.int16(self.data))

	def lowpass(self, cutoff: int, order: int) -> None:
		self.audiopass('low', cutoff, order)

	def highpass(self, cutoff: int, order: int) -> None:
		self.audiopass('high', cutoff, order)
	
	def bandpass(self, cutoff: tuple[int, int], order: int) -> None:
		self.audiopass('band', cutoff, order)

	def audiopass(self, type: Literal['high', 'low', 'band'], cutoff: tuple[int, int] | int, order: int) -> None:
		match type:
			case 'high' | 'low':
				if not isinstance(cutoff, int):
					raise TypeError("cutoff must be an int")
				bound = cutoff / self.nyquist_freq
			case 'band':
				if not isinstance(cutoff, tuple) or not isinstance(cutoff[0], int) or not isinstance(cutoff[1], int):
					raise TypeError("cutoff must be a tuple[int, int]")
				bound = (cutoff[0] / self.nyquist_freq, cutoff[1] / self.nyquist_freq)
			case _:
				raise ValueError("type must be one of ('high', 'low', 'band')")
		b, a = signal.butter(order, bound, btype=type)
		self.data = signal.filtfilt(b, a, self.data, axis=0)

	def remove_quiet(self, threshold_prop: float, window = 1) -> None:
		int_thresh = threshold_prop * np.max(self.data)
		window_view = np.lib.stride_tricks.sliding_window_view(self.data, window)
		self.data[np.where(np.abs(self.data) < int_thresh)] = 0

def average_channels(data: np.ndarray) -> np.ndarray:
	if data.ndim == 1:
		return data
	return data[0:,0] // 2 + data[0:,1] // 2
