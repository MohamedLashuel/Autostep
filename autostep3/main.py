from util import NDIntArray, sample2note, separate_drums
from sys import argv, stderr
import soundfile as sf
import better_aubio

def main():
	if len(argv) != 2:
		print(f"Usage: {argv[0]} <audio_file>", file=stderr)
		exit(1)

	drums_path = separate_drums(argv[1])
	samplerate = sf.info(drums_path).samplerate

	tempo = better_aubio.tempo_cli(drums_path)
	onsets = better_aubio.onset(drums_path, 'energy')

	onsets_sixteenth_notes: NDIntArray = sample2note(onsets, samplerate, tempo, 16)
	print(onsets_sixteenth_notes)

	# TODO: do something with this rhythm

# Call main() ONLY when this module is EXECUTED and not IMPORTED.
if __name__ == "__main__":
	main()
