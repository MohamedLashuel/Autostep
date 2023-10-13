from code import interact
from Song import Song
from array2chart import *
from detect import *
import numpy as np

np.set_printoptions(precision=3)

song = Song('drums.wav', offset = -0.095)

interact(local=globals())
