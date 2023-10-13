from code import interact
from song import Song
import numpy as np

np.set_printoptions(precision=3)

song = Song('test_audio/drums.wav')

interact(local=globals())
