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

class SscChart:
	def __init__(self,
		difficulty: str,
		meter: int,
		stepstype: str = "dance-single",
		description: Optional[str] = None,
		notes: list[str] = []
	):
		self.difficulty = difficulty
		self.meter = meter
		self.stepstype = stepstype
		self.description = description
		self.notes = notes

class SscFile:
	@staticmethod
	def open(filename: str) -> 'SscFile':
		with open(filename, "r") as file:
			file_text = file.read()
		
		def find_value(key: str):
			key = f"#{key}:"
			index = file_text.index(key) + len(key)
			return file_text[index : file_text.index(";", index)]
		
		return SscFile(
			title=find_value("TITLE"),
			music_filename=find_value("MUSIC"),
			offset=find_value("OFFSET"),
			artist=find_value("ARTIST"),
			bg_filename=find_value("BACKGROUND")
		)

		# charts = []
		# while True:
		# 	match file_text.find("//-----"):
		# 		case -1:
		# 			break
		# 		case chart_idx:

	def __init__(self,
		title: str,
		music_filename: str,
		bpm: int,
		offset: float,
		artist: Optional[str] = None,
		bg_filename: Optional[str] = None,
		charts: list[SscChart] = []
	):
		self.title = title
		self.music_filename = music_filename
		self.bpm = bpm
		self.offset = offset
		self.artist = artist
		self.bg_filename = bg_filename
		self.charts = charts
	
	def save_as(self, filename: str):
		with open(filename, "w") as file:
			write_attr = lambda key, value: file.write(f"#{key}:{value};\n")
			write_attr("VERSION", "0.83")
			write_attr("TITLE", self.title)
			write_attr("ARTIST", self.artist)
			write_attr("MUSIC", self.music_filename)
			if self.bg_filename is not None:
				write_attr("BACKGROUND", self.bg_filename)
			write_attr("OFFSET", str(self.offset))
			write_attr("BPMS", "0.000={3f}")
			for chart in self.charts:
				file.write(f"//--------------- {chart.stepstype} -----------------")
				#write_attr("NOTEDATA", "")
				write_attr("STEPSTYPE", chart.stepstype)
				write_attr("DIFFICULTY", chart.difficulty)
				write_attr("METER", chart.meter)
				write_attr("NOTES", "\n")
				for line in chart.notes:
					file.write(line + "\n")
				file.write(";\n")

def create_file(
	ssc_file: str,
	*,
	music_filename: str,
	title: str,
	artist: str,
	bpm: int,
	offset: float,
	rating: int, # diff rating
	diff_position: int, # position in the ITG diff selector
	chart_file: str,
	bg_filename: Optional[str] = None,
) -> None:
	attributes = DEFAULT_ATTRS.copy()

	# new_attributes = {'music': audio_file, 'bpms': f'0.000={bpm}', 'offset': offset}

	# attributes.update(new_attributes)

	# attribute_text = attributeText(attributes)
	# chart_text = chartText(chart_file)

	# text = attribute_text + chart_text

	with open(ssc_file, 'w') as file:
		write_attr = lambda key, value: file.write(f"#{key}:{value};\n")
		write_attr("VERSION", "0.83")
		write_attr("TITLE", title)
		write_attr("ARTIST", artist)
		write_attr("MUSIC", music_filename)
		if bg_filename is not None:
			write_attr("BACKGROUND", bg_filename)
		write_attr("OFFSET", str(offset))
		write_attr("BPMS", "0.000={3f}")

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
