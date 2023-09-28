from obj import *
from scipy import signal

# Detection functions take the song as the first parameter
# and all parameters after must be integers
# And must return a ndarray of samples

def scipyPeaks(song : Song, threshold : int, distance : int) -> np.ndarray:
    return signal.find_peaks(song.data, 
        threshold = threshold, distance = distance)[0]