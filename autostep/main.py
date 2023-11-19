import better_aubio, cmdline, ssc, util
import soundfile as sf
import autochart.inout

def main():
	args = cmdline.arg_parser.parse_args()

	drums_path, audio_file_name, audio_file_ext = util.separate_drums(args.audio_file)
	samplerate = sf.info(drums_path).samplerate

	onsets = better_aubio.onset(drums_path, args.onset_method)

	if args.bpm is None:
		args.bpm = better_aubio.tempo_cli(args.audio_file)

	match args.sample2note_method:
		case "default":
			onsets_sixteenth_notes = util.sample2note(onsets, samplerate, args.bpm, args.division)
		case "round":
			onsets_sixteenth_notes = util.sample2note_round(onsets, samplerate, args.bpm, args.division)
		case "offset":
			onsets_sixteenth_notes = util.sample2note_offset(onsets, samplerate, args.bpm, args.offset, args.division)
		case "round+offset":
			onsets_sixteenth_notes = util.sample2note_round_offset(onsets, samplerate, args.bpm, args.offset, args.division)

	util.make_chart_code(onsets_sixteenth_notes, 16, args.code_file) # type: ignore
	autochart.inout.convertToSSC(args.code_file, args.chart_file)

	ssc.write(audio_file_name + audio_file_ext, args.bpm, args.offset, 1, 0, args.chart_file, args.output_file)
	autochart.inout.injectSSCToChart(args.chart_file, args.output_file, 1)

# Call main() ONLY when this module is EXECUTED and not IMPORTED.
if __name__ == "__main__":
	main()
