from typing import Callable
from numpy.typing import NDArray
import numpy as np

NDFloatArray = NDArray[np.float_]
NDIntArray = NDArray[np.int_]

"""
Converts a stereo waveform to mono, by taking the maximum of the 2 channels.
"""
stereo2mono = lambda audio: np.max(audio, axis=1)
stereo2mono: Callable[[NDFloatArray], NDFloatArray]

def cutoff_samples(samples: NDFloatArray, cutoff_threshold: float) -> None:
	"""
	Sets the elements of `samples` to 0 where `|sample| < cutoff_threshold`.

	Requires that `len(samples.shape) == 1`.
	"""
	if len(samples.shape) > 1:
		raise ValueError("len(samples.shape) > 1")
	for r in range(samples.shape[0]):
		if abs(samples[r]) < cutoff_threshold:
			samples[r] = 0
