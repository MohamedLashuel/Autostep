import subprocess, os, shutil
try:
	import better_aubio, cmdline, ssc, util
except ModuleNotFoundError:
	from autostep import better_aubio, cmdline, ssc, util
import soundfile as sf
import autochart.inout

def main():
	args = cmdline.arg_parser.parse_args()
	drums_path, audio_file_name, audio_file_ext = util.separate_drums(args.audio_file, sep_path=args.separated_path, force=args.force_separate)

	makeOutDirectory(args.output_dir, args.overwrite)

	# Even if it's already ogg, we need to remove the path at the start
	new_audio_file = audio_file_name + ".ogg"

	copyAudioFile(args.audio_file, audio_file_ext, new_audio_file, args.output_dir)

	args.audio_file = new_audio_file
	
	samplerate = sf.info(drums_path).samplerate
	bpm, offset = getBpmOffset(args, drums_path)

	onsets = better_aubio.onset(drums_path, args.onset_method)

	onsets_notes = util.sample2note(onsets, samplerate, bpm, offset, args.division)

	util.make_chart_code(onsets_notes, args.division, args.code_file) # type: ignore
	autochart.inout.convertToSSC(args.code_file, args.chart_file)

	ssc_path = f"{args.output_dir}/{audio_file_name}.ssc"
	ssc.write(args.audio_file, bpm, offset, 1, 0, args.chart_file, ssc_path)
	autochart.inout.injectSSCToChart(args.chart_file, ssc_path, 1)

def makeOutDirectory(dir: str, force: bool) -> None:
	if dir == ".": return

	if os.path.exists(dir):
		if force:
			print(f"Deleting directory {dir}")
			shutil.rmtree(dir)
		else:
			print("Folder already exists. Use a different folder, delete it, or use the --overwrite option")
			quit(1)
	os.mkdir(dir)

def getBpmOffset(args, audio_path) -> tuple[float, float]:
	if args.bpm is not None and args.offset is not None:
		return args.bpm, args.offset
	
	bpm, offset = better_aubio.vortex_cli(audio_path)
	if args.bpm is not None: bpm = args.bpm
	if args.offset is not None: offset = args.offset

	return bpm, offset

def copyAudioFile(audio_path, extension, new_path, dir):
	if extension == ".ogg" and dir != ".":
		subprocess.run(("cp", audio_path, dir))
	else:
		subprocess.run(("ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", audio_path, f"{dir}/{new_path}"))

# Call main() ONLY when this module is EXECUTED and not IMPORTED.
if __name__ == "__main__":
	main()
