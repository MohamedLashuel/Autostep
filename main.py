from array2chart import *
import test
import code
from detect import *

np.set_printoptions(precision=3)

song = Song('test_audio/drums.wav', bpm = 128)

print(test.optimize(
    song,
    test.thirtysecondtest,
    aubioPeaks,
    ([2 ** (i + 8) for i in range(11)],
     [200])
))