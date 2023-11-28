import better_aubio
from typing import Any
import argparse

arg_parser = argparse.ArgumentParser(description="Generate an ITGMania chart (.ssc) from an audio file containing music.")

# the inner dicts conform to ArgumentParser.add_argument's keyword args
ARGUMENTS: dict[str, dict[str, Any]] = {
	"audio_file": {
		"help": "Path to an audio file, typically containing music"
	},
	"output": {
		"help": "The folder which contents will be outputted to"
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
	},
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
	"--sample2note_method": {
		"choices": ("default", "round", "offset", "round+offset"),
		"default": "round+offset",
		"help": "The sample2note implementation to use"
	},
	"--code_file": {
		"default": "tmp/autostep.ac",
		"help": "Where to store the Autochart code"
	},
	"--chart_file": {
		"default": "tmp/autostep.ssc.notes",
		"help": "Where to store the SSC notes"
	}
}

for key, value in ADVANCED_OPTS.items():
	advanced_options.add_argument(key, **value)
