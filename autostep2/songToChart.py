from imports import *
from song import *
from aubio import aubioPeaks

def basicChartCode(beats: list[np.int16]) -> str:
	beats = list(set(beats))
	txt = ''
	has_beat = [(n in beats) for n in range(max(beats))]
	i = 0
	for tf in has_beat:
		if i % DIVISION == 0:
			txt += '/'
		if tf:
			txt += 'n'
		else:
			txt += '.'
		i += 1
	return txt

def songToChart(song: Song)
	peaks = aubioPeaks(song, 1024, 512, 1)
	peaksToChart(peaks, song)
	
def peaksToChart(peaks: np.ndarray, song: Song) -> None:
	beat_numbers = samplesToBeatNumbers(peaks)
	rounded_beats = np.int16(np.round(beat_numbers))
	chart_code = basicChartCode(rounded_beats)
	writeTxt('test_output/code.txt', chart_code)

def samplesToBeatNumbers(peaks: np.ndarray) -> np.ndarray:
	offset_seconds = peaks / song.samplerate + song.offset
	fourth_beats = offset_seconds / 60 * song.bpm
	beat_numbers = fourth_beats / 4 * DIVISION
	
	return beat_numbers