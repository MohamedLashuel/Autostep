from typing import Any, Callable

DEFAULT_ATTRIBUTES = {
	"VERSION": 0.83,
	"SAMPLESTART": 0.000,
	"SAMPLELENGTH": 0.000,
	"OFFSET": 0.000,
	"BPMS": '0.000=120.000'
}

DIFFICULTY_NAMES = "Beginner", "Easy", "Medium", "Hard", "Challenge"

make_attribute_text: Callable[[dict[str, Any]], str]
make_attribute_text = lambda attributes: "\n".join(f"#{item[0]}:{item[1]};" for item in attributes.items())

def make_chart_text(chart_filepath: str, rating: int, diff_position: int):
	difficulty = DIFFICULTY_NAMES[diff_position]
	with open(chart_filepath, "r") as file:
		notes = file.read()
	return f"""//--------------- dance-single -  ----------------
#NOTEDATA:;
#STEPSTYPE:dance-single;
#DESCRIPTION:;
#DIFFICULTY:{difficulty};
#METER:{rating};
#RADARVALUES:0,0,0,0,0;
#NOTES:
{notes}
;"""

def write(
	audio_file: str,
	bpm: float,
	offset: float | str,
	rating: int,
	difficulty_pos: int,
	chart_file: str,
	output_file: str
) -> None:
	attributes = DEFAULT_ATTRIBUTES.copy()
	attributes.update({"MUSIC": audio_file, "BPMS": f"0.000={bpm}", "OFFSET": offset})
	attribute_text = make_attribute_text(attributes)
	chart_text = make_chart_text(chart_file, rating, difficulty_pos)
	with open(output_file, "w") as f:
		f.write(attribute_text + "\n" + chart_text)
