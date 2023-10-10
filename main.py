from code import interact
from Song import Song
import numpy as np

np.set_printoptions(precision=3)

song = Song('drums.wav', bpm=128, offset = -0.095)

interact(local=globals())
