from array2chart import *
import test
import code
from detect import *

np.set_printoptions(precision=3)

song = Song('drums.wav', bpm = 128, offset = -0.095)

code.interact(local = globals())

import sys
sys.stdout = open('aubioOptimize2.txt', 'w')
print(test.optimize(song,
              test.thirtysecondtest,
              aubioPeaks,
              [512, 1024, 2048],
               [256, 512],
               range(9)))

sys.stdout.close()