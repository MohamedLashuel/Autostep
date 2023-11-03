from util import make_chart_code, sample2note, separate_drums
from sys import argv, stderr
import soundfile as sf
import better_aubio
from autochart.inout import convertToSSC, injectSSCToChart

def main():
	if len(argv) != 2:
		print(f"Usage: {argv[0]} <audio_file> <difficulties>", file=stderr)
		exit(1)

	drums_path, audio_file_name = separate_drums(argv[1])
	samplerate = sf.info(drums_path).samplerate

	tempo = better_aubio.tempo_cli(drums_path)
	onsets = better_aubio.onset(drums_path, 'energy')
	onsets_sixteenth_notes = sample2note(onsets, samplerate, tempo, 16)
	make_chart_code(onsets_sixteenth_notes, 16, "code.txt")
	convertToSSC("code.txt", "chart.txt")
	injectSSCToChart("chart.txt", "generated/" + audio_file_name + ".ssc", 2)

# Call main() ONLY when this module is EXECUTED and not IMPORTED.
if __name__ == "__main__":
	main()
