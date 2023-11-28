import better_aubio, cmdline, ssc, util, os
import soundfile as sf
import autochart.inout

def main():
	args = cmdline.arg_parser.parse_args()

	drums_path, audio_file_name, audio_file_ext = util.separate_drums(args.audio_file)

	os.mkdir(args.output)
	os.chdir(args.output)

	new_audio_file = f'{audio_file_name}.ogg'
	if audio_file_ext == '.ogg':
		os.popen(f'cp ../{args.audio_file} .')
	else:
		better_aubio.shell_exec(f'ffmpeg -i ../{args.audio_file} {new_audio_file}')
	
	args.audio_file = new_audio_file
	drums_path = f'../{drums_path}'
	args.code_file = f'../{args.code_file}'
	args.chart_file = f'../{args.chart_file}'
	
	samplerate = sf.info(drums_path).samplerate

	onsets = better_aubio.onset(drums_path, args.onset_method)

	if args.bpm is None or args.offset is None:
		bpm, offset = better_aubio.vortex_cli(drums_path)
		if args.bpm is None: args.bpm = bpm
		if args.offset is None: args.offset = offset

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

	ssc.write(args.audio_file, args.bpm, args.offset, 1, 0, args.chart_file, f'{audio_file_name}.ssc')
	autochart.inout.injectSSCToChart(args.chart_file, f'{audio_file_name}.ssc', 1)

# Call main() ONLY when this module is EXECUTED and not IMPORTED.
if __name__ == "__main__":
	main()
