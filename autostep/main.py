from code import interact
from song import Song
import numpy as np
from detect import *
from array2chart import *
import test

np.set_printoptions(precision=3)

song = Song('test_audio/drums.wav', bpm = 128, offset = -0.095)

arrayToChart(aubioPeaks(song, 1024, 512, 1), song)