from copy import deepcopy
from typing import Literal
from waveform import Waveform
from .better_aubio import tempo, onset

class Song:
	def __init__(self, filename: str):
		self.waveform = Waveform.from_file(filename)
		self.bpm = tempo(filename)
		self.beats = onset(filename)
	
	def filter(self, filter_type: Literal['low', 'high', 'band'], cutoff: int | tuple[int, int], order: int) -> 'Song':
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
				if not isinstance(cutoff, tuple) or not isinstance(cutoff[0], int) or not isinstance(cutoff[1], int):
					raise TypeError("cutoff must be a 2-tuple of ints!")
				new_song.waveform = self.waveform.bandpass(cutoff[0], cutoff[1], order)
		return new_song
	
	def save_to_file(self, filename: str) -> None:
		self.waveform.save_to_file(filename)
