from typing import Optional

ATTR_NAMES = [
	'version', 'title', 'subtitle', 'artist', 'titletranslit',
	'subtitletranslt', 'artisttranslit', 'genre', 'credit', 'music',
	'banner', 'background', 'cdtitle', 'samplestart', 'samplelength',
	'selectable', 'offset', 'bpms', 'stops', 'bgchanges', 'fgchanges'
]

DEFAULT_ATTRS = {
	'version': 0.83,
	'samplestart': 0.000,
	'samplelength': 0.000,
	'offset': 0.000,
	'bpms': '0.000=120.000'
}

DIFFICULTY_NAMES = ["Beginner", "Easy", "Medium", "Hard", "Challenge"]

def create_file(
	audio_file: str,
	bpm: float,
	offset: str,
	rating: int,
	difficulty_pos: int,
	chart_file: str,
	output_file: str
) -> None:
	attributes = DEFAULT_ATTRS.copy()

	new_attributes = {'music': audio_file, 'bpms': f'0.000={bpm}', 'offset': offset}

	attributes.update(new_attributes)

	attribute_text = attributeText(attributes)
	chart_text = chartText(chart_file, rating, difficulty_pos)

	text = attribute_text + '\n' + chart_text

	with open(output_file, 'w') as f:
		f.write(text)

def attributeText(attributes):
	def attributeToLine(item):
		return f'#{item[0].upper()}:{item[1]};'

	lines = [attributeToLine(item) for item in attributes.items()]

	return '\n'.join(lines)

def chartText(chart_filepath: str, rating: int, diff_position: int):
	difficulty = DIFFICULTY_NAMES[diff_position]

	return f"""//--------------- dance-single -  ----------------
#NOTEDATA:;
#STEPSTYPE:dance-single;
#DESCRIPTION:;
#DIFFICULTY:{difficulty};
#METER:{rating};
#RADARVALUES:0,0,0,0,0;
#NOTES:
{loadTxt(chart_filepath)}
;"""

def loadTxt(chart_filepath: str):
	with open(chart_filepath, 'r') as f:
		return f.read()