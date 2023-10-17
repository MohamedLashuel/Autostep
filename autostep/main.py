from code import interact
from song import Song
import numpy as np
from detect import *
from array2chart import *
import test

np.set_printoptions(precision=3)

song = Song('test_audio/vocals.wav', bpm = 128, offset = -0.095)
song.remove_quiet(0.25)

if __name__ == '__main__':
    interact(local=globals())
