import numpy as np
from scipy.io import wavfile
from scipy import signal
from copy import deepcopy
from typing import Literal
from Waveform import Waveform
from audio_tempo_cli import aubio_tempo

class Song:
	def __init__(self, filepath: str, offset: float):
		self.waveform = Waveform.from_file(filepath)
		self.bpm = aubio_tempo(filepath)
		self.offset = offset
		self.filepath = filepath

	def sample_rate(self) -> int: return self.waveform.sample_rate
	def data(self) -> int: return self.waveform.data
	
	def filter(self, filter_type: Literal['low', 'high', 'band'], cutoff: int | tuple[int], order: int) -> 'Song':
		new_song = deepcopy(self)
		match filter_type:
			case 'low':
				if not isinstance(cutoff, int):
					raise TypeError("cutoff must be an int!")
				new_song.waveform = self.waveform.lowpass(cutoff, order)
			case 'high':
				if not isinstance(cutoff, int):
					raise TypeError("cutoff must be an int!")
				new_song.waveform = self.waveform.highpass(cutoff, order)
			case 'band':
				if not isinstance(cutoff, tuple):
					raise TypeError("cutoff must be a 2-tuple of ints!")
				new_song.waveform = self.waveform.bandpass(cutoff[0], cutoff[1], order)
		return new_song
	
	def save_to_file(self, filename: str) -> None:
		self.waveform.save_to_file(filename)
