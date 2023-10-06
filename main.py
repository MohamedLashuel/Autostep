from array2chart import *
import code
from detect import *

np.set_printoptions(precision=3)

song = Song('drums.wav', bpm=128, offset = -0.095)

low_song = audiopass(song, 'lowpass', 300, 1, 'low.wav')
high_song = audiopass(song, 'highpass', 300, 1, 'high.wav')

code.interact(local=globals())
