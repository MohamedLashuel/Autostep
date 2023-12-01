import subprocess
import better_aubio, cmdline, ssc, util, os
import soundfile as sf
import autochart.inout

def main():
	args = cmdline.arg_parser.parse_args()
	drums_path, audio_file_name, audio_file_ext = util.separate_drums(args.audio_file, sep_path=args.separated_path, force=args.force_separate)

	if args.output_dir != ".":
		os.mkdir(args.output_dir)

	# TODO: Figure out which extensions need correcting
	if audio_file_ext == ".mp3" and args.output_dir != ".":
		subprocess.run(("cp", args.audio_file, args.output_dir))
	else:
		new_audio_file = audio_file_name + ".ogg"
		subprocess.run(("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", args.audio_file, f"{args.output_dir}/{new_audio_file}"))
		args.audio_file = new_audio_file

	samplerate = sf.info(drums_path).samplerate
	onsets = better_aubio.onset(drums_path, args.onset_method)

	if args.bpm is None or args.offset is None:
		bpm, offset = better_aubio.vortex_cli(drums_path)
		if args.bpm is None: args.bpm = bpm
		if args.offset is None: args.offset = offset

	onsets_notes = util.sample2note(onsets, samplerate, args.bpm, args.offset, args.division)

	util.make_chart_code(onsets_notes, 16, args.code_file) # type: ignore
	autochart.inout.convertToSSC(args.code_file, args.chart_file)

	ssc_path = f"{args.output_dir}/{audio_file_name}.ssc"
	ssc.write(args.audio_file, args.bpm, args.offset, 1, 0, args.chart_file, ssc_path)
	autochart.inout.injectSSCToChart(args.chart_file, ssc_path, 1)

# Call main() ONLY when this module is EXECUTED and not IMPORTED.
if __name__ == "__main__":
	main()
