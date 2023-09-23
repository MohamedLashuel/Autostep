from typing import Iterable
from autochart.inout import writeTxt, convertToSSC, injectSSCToChart
import numpy as np

DIVISION = 16

def makeChartCode(beats: Iterable[int]) -> str:
	beats = list(set(beats))
	txt = '1:'
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
	writeTxt('code.txt', chart_code)
	convertToSSC('code.txt', 'chart.txt')
	injectSSCToChart('chart.txt', destination, 1)

def arrayToChart(peaks: np.ndarray, bpm: int, samplerate: int) -> None:
	num_beats = peaks / samplerate / 60 * bpm * DIVISION / 4
	rounded_beats = np.int16(np.round(num_beats))
	chart_code = makeChartCode(rounded_beats)
	injectChartCode(chart_code, 'TurnOffTheLights.ssc')
