import numpy as np
from scipy.io import wavfile
from typing import Iterable, Callable

class Song:
    def __init__(self, filepath: str, bpm: float):
        self.samplerate, self.data = wavfile.read(filepath)

        self.filepath = filepath

        self.data = averageChannels(self.data)

        self.bpm = bpm

def averageChannels(data: np.ndarray) -> np.ndarray:
    return data[0:,0]/2 + data[0:,1]/2