from typing import Optional

ATTR_NAMES = [
	'version', 'title', 'subtitle', 'artist', 'titletranslit',
	'subtitletranslt','artisttranslit','genre','credit','music',
	'banner','background','cdtitle','samplestart','samplelength',
	'selectable','offset','bpms','stops','bgchanges','fgchanges'
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
	ssc_file: str,
	music_file
	title: str,
	artist: str,
	tempo: int,
	offset: float,
	rating: int, # diff rating
	diff_position: int, # position in the ITG diff selector
	chart_file: str,
	*,
	bg: Optional[str],
) -> None:
	attributes = DEFAULT_ATTRS.copy()

	new_attributes = {'music': music_file, 'bpms': f'0.000={bpm}', 'offset': offset}

	attributes.update(new_attributes)

	attribute_text = attributeText(attributes)
	chart_text = chartText(chart_file)

	text = attribute_text + chart_text

	with open(ssc_file, 'w') as f:
		f.write(ssc_text)

def attributeText(attributes):
	def attributeToLine(item):
		return f'#{item[0].upper}:{item[1]};'

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
