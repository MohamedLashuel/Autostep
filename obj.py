import numpy as np
from scipy.io import wavfile
from scipy import signal
from copy import deepcopy

class Song:
    def __init__(self, filepath: str, bpm: float, offset: float):
        self.samplerate, self.data = wavfile.read(filepath)
        self.nyquist_freq = self.samplerate * 0.5

        self.filepath = filepath

        self.data = averageChannels(self.data)
        
        self.bpm = bpm
        self.offset = offset

    def saveToFile(self, filename: str = 'audio.wav') -> None:
        # Convert to integer for PCM format. HAS TO BE int16
        data = np.int16(self.data)
        wavfile.write(filename, self.samplerate, data)

def averageChannels(data: np.ndarray) -> np.ndarray:
    if data.ndim == 1: return data
    return data[0:,0]//2 + data[0:,1]//2

def audiopass(song: Song, type: str, cutoff_freq: tuple[int] | int, 
        order: int, filepath = 'audio.wav') -> Song:
    match type:
        case 'highpass' | 'lowpass':
            bound = cutoff_freq / song.nyquist_freq
        case 'bandpass':
            bound = (cutoff_freq[0] / song.nyquist_freq, 
                cutoff_freq[1] / song.nyquist_freq)
        case _:
            raise ValueError(f'audiopass given type {type} which is invalid')

    b, a = signal.butter(order, bound, btype=type)
    song_copy = deepcopy(song)

    song_copy.data = signal.filtfilt(b, a, song.data, axis=0)

    song_copy.saveToFile(filepath)
    song_copy.filepath = filepath

    return song_copy
