from numpy.typing import NDArray
from spleeter.audio import Codec
from os import path
import numpy as np

NDFloatArray = NDArray[np.float_]
NDIntArray = NDArray[np.int_]

stereo2mono = lambda audio: np.max(audio, axis=1)
"""
Converts a 2D Numpy array containing stereo audio into a 1D array by taking the max of each sample.

## Parameters
```
audio: NDFloatArray
```

## Returns
```
audio: NDFloatArray
```
"""

sample2note = lambda sample, samplerate, tempo, note_division = 16: \
	np.int_((sample / samplerate) / 60 * tempo * note_division / 4)

sample2note_round = lambda sample, samplerate, tempo, note_division = 16: \
	np.int_(np.round((sample / samplerate) / 60 * tempo * note_division / 4))

sample2note_offset = lambda sample, samplerate, tempo, offset = 0, note_division = 16: \
	np.int_((sample / samplerate + offset) / 60 * tempo * note_division / 4)

sample2note_round_offset = lambda sample, samplerate, tempo, offset = 0, note_division = 16: \
	np.int_(np.round((sample / samplerate + offset) / 60 * tempo * note_division / 4))
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

## Parameters
```
sample: NDFloatArray | float
samplerate: int
tempo: float
offset: float
note_division: int
```

## Returns
```
sample: NDFloatArray | float
```
"""

def cutoff_samples(
	samples: NDFloatArray,
	cutoff_threshold: float
) -> NDFloatArray:
	"""
	Returns a copy of `samples` where every `sample` is zero if `|sample| < cutoff_threshold`.

	Requires that `len(samples.shape) == 1` (one-dimensional).

	## Returns
	```
	samples: NDFloatArray
	```
	"""
	if len(samples.shape) != 1:
		raise ValueError("`samples` is not a 1D array")
	samples = samples.copy()
	for i in range(samples.shape[0]):
		if abs(samples[i]) < cutoff_threshold:
			samples[i] = 0
	return samples

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
) -> tuple[str, str, str]:
	audio_file_name = audio_path[highest_index(audio_path, "/") + 1 : highest_index(audio_path, ".")]
	audio_file_ext = audio_path[highest_index(audio_path, ".") :]
	drums_path = path.join(sep_path, audio_file_name, "drums." + codec)
	if force or not path.exists(drums_path):
		from spleeter.separator import Separator
		separator = Separator("spleeter:5stems")
		separator.separate_to_file(audio_path, sep_path, codec=codec, synchronous=True)
	return drums_path, audio_file_name, audio_file_ext

def make_chart_code(
	onsets: NDIntArray,
	division: int,
	filename: str
) -> None:
	with open(filename, "w") as file:
		for i in range(max(onsets)):
			if i % division == 0:
				file.write("/")
			file.write("n" if i in onsets else ".")
