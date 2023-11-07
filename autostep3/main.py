from util import cut_offset, make_chart_code, sample2note, separate_drums
from sys import argv, stderr
import soundfile as sf
import better_aubio
from ssc import *
from autochart.inout import convertToSSC, injectSSCToChart

def main():
	if len(argv) != 4:
		print(f"Usage: {argv[0]} <audio_file> <bpm> <offset> <output_file>",
		 file=stderr)
		exit(1)
	
	audio_file = argv[1]
	bpm = int(argv[2])
	offset = -float(argv[3])
	output_file = argv[4]

	if offset > 0:
		cut_offset(audio_file, audio_file + "-offset.mp3", offset)
		audio_file += "-offset.mp3"

	drums_path, audio_file_name = separate_drums(audio_file)
	samplerate = sf.info(drums_path).samplerate

	onsets = better_aubio.onset(drums_path, 'energy')
	onsets_sixteenth_notes = sample2note(onsets, samplerate, bpm, 16)
	make_chart_code(onsets_sixteenth_notes, 16, "code.txt")
	convertToSSC("code.txt", "chart.txt")
	injectSSCToChart("chart.txt", "generated/" + audio_file_name + ".ssc", 2)

	create_file('audio_file_name', bpm, offset, 1, 0, 'chart.txt', output_file)

# Call main() ONLY when this module is EXECUTED and not IMPORTED.
if __name__ == "__main__":
	main()