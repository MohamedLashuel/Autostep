from typing import Iterable
from autochart.inout import writeTxt, convertToSSC, injectSSCToChart
import numpy as np
from song import Song

DIVISION = 32

def makeChartCode(beats: Iterable[np.int16]) -> str:
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

def injectChartCode(chart_code, destination) -> None:
	writeTxt('test_output/code.txt', chart_code)
	convertToSSC('test_output/code.txt', 'test_output/chart.txt')
	injectSSCToChart('test_output/chart.txt', destination, 1)

def arrayToChart(peaks: np.ndarray, song: Song) -> None:
	beat_times = (peaks / song.samplerate + song.offset) / 60 * song.bpm * DIVISION / 4
	rounded_beats = np.int16(np.round(beat_times))
	chart_code = makeChartCode(rounded_beats)
	injectChartCode(chart_code, 'sigma.ssc')
