from autochart.inout import writeTxt, convertToSSC, injectSSCToChart
import numpy as np

DIVISION = 32

def makeChartCode(beats):
	beats = list(set(beats))
	txt = '1:'
	has_beat = [n in beats for n in range(max(beats))]
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

def injectChartCode(chart_code, destination):
	writeTxt('code.txt', chart_code)
	convertToSSC('code.txt', 'chart.txt')
	injectSSCToChart('chart.txt', destination, 1)

def arrayToChart(peaks, bpm, samplerate):
	beats = peaks / samplerate / 60 * bpm * DIVISION / 4
	rounded_beats = np.int16(np.round(beats))
	chart_code = makeChartCode(rounded_beats)
	injectChartCode(chart_code, 'TurnOffTheLights.ssc')
