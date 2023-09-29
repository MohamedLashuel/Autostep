from array2chart import *
import test
from detect import *

np.set_printoptions(precision=3)

song = Song('test_audio/drums.wav', bpm = 128)

print(test.optimize(
    song,
    test.thirtysecondtest,
    scipyPeaks,
    range(1000, 6001, 1000),
    range(500,5001,500)
))