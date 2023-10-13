from random import sample
from typing import Literal, Optional
from scipy.io import wavfile
from scipy import signal
from autostep.better_aubio import tempo
from numpy.typing import NDArray
import sounddevice as sd
import numpy as np

def average_channels(data: np.ndarray) -> np.ndarray:
	if data.ndim == 1:
		return data
	return (data[0:,0] // 2) + (data[0:,1] // 2)

class Song:
	@staticmethod
	def from_file(filename: str, offset: float) -> 'Song':
		sample_rate, data = wavfile.read(filename)
		return Song(filename=filename, sample_rate=sample_rate, data=data, offset=offset)

	def __init__(
		self, *,
		sample_rate: int,
		data: NDArray[np.int16],
		offset: float,
		filename: Optional[str] = None,
		bpm: Optional[int] = None
	) -> None:
		self.sample_rate = sample_rate

		# if len(np.shape(data)) > 1:
		# 	self.data: NDArray[np.int16] = average_channels(data)
		# else:
		self.data = data

		self.nyquist_freq = self.sample_rate * 0.5
		self.offset = offset
		self.filename = filename
		
		if bpm is None:
			if filename is None:
				self.bpm = None
			else:
				self.bpm = tempo(filename)
		else:
			self.bpm = bpm

	def save(self) -> None:
		if self.filename is None:
			raise AttributeError("This `Song` instance does not have a filename!")
		self.save_to_file(self.filename)

	def save_to_file(self, filename: str) -> None:
		# Convert to integer for PCM format. HAS TO BE int16
		wavfile.write(filename, self.sample_rate, np.int16(self.data))

	def filter(self,
		type: Literal['low', 'high', 'band'],
		cutoff: int | tuple[int, int],
		order: int
	) -> 'Song':
		match type:
			case 'high' | 'low':
				if not isinstance(cutoff, int):
					raise TypeError("cutoff must be an int!")
				b, a = signal.butter(order, cutoff / self.nyquist_freq, btype=f"{type}pass")
			case 'band':
				if not isinstance(cutoff, tuple) or not isinstance(cutoff[0], int) or not isinstance(cutoff[1], int):
					raise TypeError("cutoff must be a 2-tuple of ints!")
				band = (cutoff[0] / self.nyquist_freq, cutoff[1] / self.nyquist_freq)
				b, a = signal.butter(order, band, btype="bandpass")
		return Song(sample_rate=self.sample_rate, data=signal.filtfilt(b, a, self.data, axis=0), offset=self.offset, filename=self.filename, bpm=self.bpm)
	
	def lowpass(self, cutoff: int, order: int) -> 'Song':
		b, a = signal.butter(order, cutoff / self.nyquist_freq, btype='lowpass')
		return Song(sample_rate=self.sample_rate, data=signal.filtfilt(b, a, self.data, axis=0), offset=self.offset, filename=self.filename, bpm=self.bpm)

	def highpass(self, cutoff: int, order: int) -> 'Song':
		b, a = signal.butter(order, cutoff / self.nyquist_freq, btype='highpass')
		return Song(sample_rate=self.sample_rate, data=signal.filtfilt(b, a, self.data, axis=0), offset=self.offset, filename=self.filename, bpm=self.bpm)

	def bandpass(self, cutoffs: tuple[int, int], order: int) -> 'Song':
		band = (cutoffs[0] / self.nyquist_freq, cutoffs[1] / self.nyquist_freq)
		b, a = signal.butter(order, band, btype='bandpass')
		return Song(sample_rate=self.sample_rate, data=signal.filtfilt(b, a, self.data, axis=0), offset=self.offset, filename=self.filename, bpm=self.bpm)

	def play(self) -> None:
		sd.play(self.data, samplerate=self.sample_rate)

	def stop(self) -> None:
		sd.stop()
