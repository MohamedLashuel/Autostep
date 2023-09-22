import code
import numpy as np
from scipy.io import wavfile
from scipy import signal

np.set_printoptions(precision = 3)

sample_rate, dt = wavfile.read('drums.wav')
dt = dt[0:,0]/2 + dt[0:,1]/2

def getPeaks(threshold = 0, distance = 0):
    return signal.find_peaks(dt, threshold = threshold, distance = distance)[0]

bpm = 128
def s2b(samples):
    return samples / sample_rate * bpm / 60

def getNotes(threshold = 0, distance = 0):
    return s2b(getPeaks(threshold, distance)) * (2 ** 2)

fp = getPeaks(3000, 500)

import array2chart
array2chart.arrayToChart(fp, bpm, sample_rate)