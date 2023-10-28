from spleeter.separator import Separator
from spleeter.audio import Codec
from sys import argv, stderr
from os import path
import soundfile as sf
import better_aubio

# Separation destination directory
SEP_DEST_DIR = "separated_audio"

# Codec to save separated audio in
CODEC = Codec.MP3

# Whether to force separation
FORCE_SEP = False

if len(argv) != 2:
	print(f"Usage: {argv[0]} <audio_file>", file=stderr)
	exit(1)

def highest_index(s: str, target: str) -> int:
	for i in range(len(s) - 1, -1, -1):
		if s[i] == target:
			return i
	raise Exception("target not found in s!")

audio_path = argv[1]
audio_path_without_ext = audio_path[:highest_index(audio_path, '.')]

if FORCE_SEP or not path.exists(path.join(SEP_DEST_DIR, audio_path_without_ext)):
	separator = Separator("spleeter:5stems")
	separator.separate_to_file(audio_path, SEP_DEST_DIR, codec=CODEC, synchronous=True)

drums_path = path.join(SEP_DEST_DIR, audio_path_without_ext, "drums." + CODEC)
audio, samplerate = sf.read(drums_path)

tempo = better_aubio.tempo_cli(drums_path)
onsets = better_aubio.onset(drums_path, 'energy')

# TODO: implement musical note subdivision
