from spleeter.audio import Codec
from sys import argv, stderr
import soundfile as sf
from os import path
import better_aubio
from util import NDIntArray, sample2note, highest_index

### Constants (we can paramaterize these later)

# Spleeter: separation destination directory
SEP_DEST_DIR = "separated_audio"

# Spleeter: separated audio codec
# MP3s save a lot of space compared to WAVs, so I think this is the best default
CODEC = Codec.MP3

# Whether to separate even if already separated
FORCE_SEP = False

def main():
	if len(argv) != 2:
		print(f"Usage: {argv[0]} <audio_file>", file=stderr)
		exit(1)

	audio_path = argv[1]
	audio_path_without_ext = audio_path[:highest_index(audio_path, '.')]

	if FORCE_SEP or not path.exists(path.join(SEP_DEST_DIR, audio_path_without_ext)):
		# This import takes a while, so import it only when needed
		from spleeter.separator import Separator
		separator = Separator("spleeter:5stems")
		separator.separate_to_file(audio_path, SEP_DEST_DIR, codec=CODEC, synchronous=True)

	drums_path = path.join(SEP_DEST_DIR, audio_path_without_ext, "drums." + CODEC)
	samplerate = sf.info(drums_path).samplerate

	tempo = better_aubio.tempo_cli(drums_path)
	onsets = better_aubio.onset(drums_path, 'energy')

	onsets_sixteenth_notes: NDIntArray = sample2note(onsets, samplerate, tempo, 16)

	# TODO: do something with this rhythm

# Call main() ONLY when this module is EXECUTED and not IMPORTED.
if __name__ == "__main__":
	main()
