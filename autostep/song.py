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

    def audiopass(self, type: str, cutoff_freq: tuple[int] | int, 
        order: int, filepath = 'audio.wav') -> None:
        nyquist_freq = self.samplerate / 2
        match type:
            case 'highpass' | 'lowpass':
                bound = cutoff_freq / nyquist_freq
            case 'bandpass':
                bound = (cutoff_freq[0] / nyquist_freq, 
                    cutoff_freq[1] / nyquist_freq)
            case _:
                raise ValueError(f'audiopass given type {type} which is invalid')

        b, a = signal.butter(order, bound, btype=type)
        self.data = signal.filtfilt(b, a, self.data, axis=0)

        self.saveToFile(filepath)
        self.filepath = filepath

    def removeQuiet(self, threshold_prop: float, window = 1) -> None:
        int_thresh = threshold_prop * np.max(self.data)

        window_view = np.lib.stride_tricks.sliding_window_view(self.data, window)
        
        self.data[np.where(np.abs(self.data) < int_thresh)] = 0

def averageChannels(data: np.ndarray) -> np.ndarray:
    if data.ndim == 1: return data
    return data[0:,0]//2 + data[0:,1]//2