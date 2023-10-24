from imports import *

class Song():
    def __init__(self, filepath: str):
        self.data, self.samplerate = readWav(filepath)
        self.data = averageChannels(self.data)

        self.bpm = aubioBpm(filepath)
        self.offset = aubioOffset(filepath)

def readWav(filepath: str):
      try:
        return wavfile.read(filepath)
      except FileNotFoundError:
        print(f'ERROR: {filepath} not found')
        shutdown()
      except ValueError:
        print(f'ERROR: {filepath} needs to be a .wav file')
        shutdown()

def averageChannels(data: np.ndarray) -> np.ndarray:
	if data.ndim == 1:
		return data
	return data[0:,0] // 2 + data[0:,1] // 2