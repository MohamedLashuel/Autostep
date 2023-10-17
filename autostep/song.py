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
        max, min = np.max(self.data), np.min(self.data)
        int_thresh = threshold_prop * np.max(self.data)

        window_view = np.lib.stride_tricks.sliding_window_view(self.data, window)
        
        window_below_thresh = np.abs(window_view) < int_thresh

        indices_to_blank = np.where(np.any(window_below_thresh, axis = 1))

        self.data[indices_to_blank] = 0
        self.data[1:window] = 0
        self.data[len(self.data) - window:] = 0

def averageChannels(data: np.ndarray) -> np.ndarray:
    if data.ndim == 1: return data
    return data[0:,0]//2 + data[0:,1]//2