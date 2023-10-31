from numpy.typing import NDArray
from spleeter.audio import Codec
import numpy as np
from os import path

NDFloatArray = NDArray[np.float_]
NDIntArray = NDArray[np.int_]

stereo2mono = lambda audio: np.max(audio, axis=1)

sample2note = lambda sample, samplerate, tempo, note_division = 4: np.int_((sample / samplerate) / (60 / tempo) * (note_division / 4))
"""
Converts a sample number to a note number of a certain division.

By default, `note_division = 4`, so `sample` will be approximated to quarter notes (whole or fractional).

In general, `note_division = X` will approximate `sample` to `Y`s:
| `X` | `Y` |
|:--------:|:--------:|
| 1 | whole note |
| 2 | half note |
| 4 | quarter note |
| 8 | eighth note |
| 16 | sixteenth note |
| ... | ... |
"""

# I algebraically solved sample2note for sample and got this...
note2sample = lambda note, samplerate, tempo, note_division = 4: np.int_(samplerate * note * (60 / tempo) * (4 / note_division))

# This should return sample numbers snapped to `note_division` notes
snap_sample = lambda sample, samplerate, tempo, note_division = 4: note2sample(sample2note(sample, samplerate, tempo, note_division), samplerate, tempo, note_division)

def cutoff_samples(samples: NDFloatArray, cutoff_threshold: float) -> None:
	"""
	Sets the elements of `samples` to 0 where `|sample| < cutoff_threshold`.

	Requires that `len(samples.shape) == 1`.
	"""
	if len(samples.shape) != 1:
		raise ValueError("len(samples.shape) != 1")
	for r in range(samples.shape[0]):
		if abs(samples[r]) < cutoff_threshold:
			samples[r] = 0

def highest_index(s: str, target: str) -> int:
	"""
	Find the highest index in which `target` occurs in `s`.
	"""
	for i in range(len(s) - 1, -1, -1):
		if s[i] == target:
			return i
	return -1

def separate_drums(
	audio_path: str,
	*,
	codec = Codec.WAV,
	sep_path = "separated",
	force = False
):
	audio_file_name = audio_path[highest_index(audio_path, '/') + 1 : highest_index(audio_path, '.')]
	drums_path = path.join(sep_path, audio_file_name, "drums." + codec)
	if force or not path.exists(drums_path):
		from spleeter.separator import Separator
		separator = Separator("spleeter:5stems")
		separator.separate_to_file(audio_path, sep_path, codec=codec, synchronous=True)
	return drums_path
