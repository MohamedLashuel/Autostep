import numpy as np
from scipy.io import wavfile

class Song:
    def __init__(self, filepath: str, bpm: float, offset: float):
        self.samplerate, self.data = wavfile.read(filepath)

        self.filepath = filepath

        self.data = averageChannels(self.data)
        self.data = normalize(self.data)
        self.bpm = bpm
        self.offset = offset

def averageChannels(data: np.ndarray) -> np.ndarray:
    return data[0:,0]/2 + data[0:,1]/2

def normalize(data: np.ndarray) -> np.ndarray:
    return data / np.max(np.abs(data))