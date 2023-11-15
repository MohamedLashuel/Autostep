from typing import Any
import soundfile as sf
import better_aubio
import ssc
import autochart.inout
import util
import argparse

CODE_FILE = "/tmp/code.txt"
CHART_FILE = "/tmp/chart.txt"

arg_parser = argparse.ArgumentParser(description="Generate an ITGMania chart (.ssc) from an audio file containing music.")

# the inner dicts conform to ArgumentParser.add_argument's keyword args
ARGUMENTS: dict[str, dict[str, Any]] = {
	"audio_file": {
		"help": "Path to an audio file, typically containing music"
	},
	"output_file": {
		"help": "The file to save the ITGMania chart to, typically ending in .ssc"
	},
	"--bpm": {
		"type": float,
		"help": "Music tempo",
		"required": False
	},
	"--offset": {
		"type": float,
		"help": "Music start time relative to audio start time",
		"default": 0
	},
	"--onset_method": {
		"choices": better_aubio.ONSET_METHODS,
		# GOOD onset methods: default, complex, hfc
		# BAD onset methods: energy, phase
		"default": "default",
		"help": "The onset (beat) detection method to use"
	},
	"--sample2note_method": {
		"choices": ("default", "round", "offset", "round+offset"),
		"default": "default"
	}
}

for key, value in ARGUMENTS.items():
	arg_parser.add_argument(key, **value)

def main():
	args = arg_parser.parse_args()

	drums_path, _ = util.separate_drums(args.audio_file)
	samplerate = sf.info(drums_path).samplerate

	onsets = better_aubio.onset(drums_path, args.onset_method)

	if args.bpm is None:
		args.bpm = better_aubio.tempo_cli(args.audio_file)

	# this is here for TESTING PURPOSES, at least for now
	match args.sample2note_method:
		case "default":
			onsets_sixteenth_notes = util.sample2note(onsets, samplerate, args.bpm, 16)
		case "round":
			onsets_sixteenth_notes = util.sample2note_round(onsets, samplerate, args.bpm, 16)
		case "offset":
			onsets_sixteenth_notes = util.sample2note_offset(onsets, samplerate, args.bpm, args.offset, 16)
		case "round+offset":
			onsets_sixteenth_notes = util.sample2note_round_offset(onsets, samplerate, args.bpm, args.offset, 16)

	util.make_chart_code(onsets_sixteenth_notes, 16, CODE_FILE) # type: ignore
	autochart.inout.convertToSSC(CODE_FILE, CHART_FILE)

	ssc.write(args.audio_file, args.bpm, args.offset, 1, 0, CHART_FILE, args.output_file)
	autochart.inout.injectSSCToChart(CHART_FILE, args.output_file, 1)

# Call main() ONLY when this module is EXECUTED and not IMPORTED.
if __name__ == "__main__":
	main()
