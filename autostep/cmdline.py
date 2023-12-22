try:
	import better_aubio
except ModuleNotFoundError:
	from autostep import better_aubio

from typing import Any
import argparse

arg_parser = argparse.ArgumentParser(description="Generate a Stepmania chart (.ssc) from an audio file containing music.")

# the inner dicts conform to ArgumentParser.add_argument's keyword args
ARGUMENTS: dict[str, dict[str, Any]] = {
	"audio_file": {
		"help": "Path to an audio file, typically containing music"
	},
	"--output_dir": {
		"help": "The folder which contents will be outputted to",
		"default": "."
	},
	"--bpm": {
		"type": float,
		"help": "Music tempo",
		"required": False
	},
	"--offset": {
		"type": float,
		"help": "Music start time relative to audio start time",
		"required": False
	},
	"--division": {
		"type": int,
		"help": "Total number of notes in a measure",
		"default": 16
	}
}

for key, value in ARGUMENTS.items():
	arg_parser.add_argument(key, **value)

advanced_options = arg_parser.add_argument_group("advanced")

ADVANCED_OPTS = {
	"--onset_method": {
		"choices": better_aubio.ONSET_METHODS,
		# GOOD onset methods: default, complex, hfc
		# BAD onset methods: energy, phase
		"default": "default",
		"help": "The onset (beat) detection method to use"
	},
	"--code_file": {
		"default": "code.txt",
		"help": "Where to store the Autochart code"
	},
	"--chart_file": {
		"default": "chart.txt",
		"help": "Where to store the SSC notes"
	},
	"--separated_path": {
		"default": "separated",
		"help": "Where to store separated audio"
	},
	"--separated_path": {
		"default": "separated",
		"help": "Where to store separated audio"
	},
	"--overwrite": {
		"default": False,
		"action": "store_true",
		"help": "Force overwriting of output directory even if it already exists"
	},
	"--force_separate": {
		"default": False,
		"action": "store_true",
		"help": "Force separation of audio stems even if separated audio already exists"
	}
}

for key, value in ADVANCED_OPTS.items():
	advanced_options.add_argument(key, **value)
