from code import interact
from Song import Song
import numpy as np

np.set_printoptions(precision=3)

song = Song('drums.wav', bpm=128, offset = -0.095)

low_song = song.filter('low', 300, 1)
low_song.save_to_file('drums_lowpass.wav')

high_song = song.filter('high', 300, 1)
high_song.save_to_file('drums_highpass.wav')

interact(local=globals())
