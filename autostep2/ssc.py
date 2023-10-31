from imports import *
from song import *

class ssc:
    def __init__(self, song: Song, chart_ratings_filepaths: 
            list[tuple[int,str]], filepath: str):
        assert pathIsValid(filepath)

        self.attributes = initialAttributes()

        new_attributes = {'music': song.filepath,
                          'bpms': f'0.000={song.bpm}',
                          'offset': song.offset}
        
        self.attributes.update(new_attributes)

        self.filepath = filepath

        self.chart_ratings_filepaths = chart_ratings_filepaths

        # Remove the file extension, then grab the part after last slash
        self.name = re.sub('.\w+$', '', song.filepath)
        self.name = self.name.split('/')[-1]

    def toFile(self, filename: str = None):
        if filename is None: filename = f'{self.name}.ssc'

        attribute_text = self.attributeText()
        charts_text = self.chartsText()

        with open(filename, 'w') as f:
            f.write(attribute_text + charts_text)

    def attributeText(self):
        def attributeToLine(item):
            return f'#{item[0].upper}:{item[1]};'

        lines = [attributeToLine(item) for item in self.attributes.items()]

        return '\n'.join(lines)
    
    def chartsText(self):
        ratings = [x[0] for x in self.chart_ratings_filepaths]
        filepaths = [x[1] for x in self.chart_ratings_filepaths]
        diff_rankings = [i for i in len(self.chart_ratings_filepaths)]

        chartTexts = map(chartText, ratings, filepaths, diff_rankings)

        return '\n'.join(chartTexts)

def initialAttributes() -> dict:
    names = ['version', 'title', 'subtitle', 'artist', 'titletranslit',
             'subtitletranslt','artisttranslit','genre','credit','music',
             'banner','background','cdtitle','samplestart','samplelength',
             'selectable','offset','bpms','stops','bgchanges','fgchanges']
    
    attributes = {name : '' for name in names}

    overwrite = {'version': 0.83, 
                 'samplestart': 0.000, 
                 'samplelength': 0.000, 
                 'offset': 0.000, 
                 'bpms': '0.000=120.000'}
    
    attributes.update(overwrite)

    return attributes

def chartText(chart_filepath: str, chart_rating: int, diff_pos: int):
    assert diff_pos > 0 and diff_pos <= 5
    difficulty_names = ["Beginner", "Easy", "Medium", "Hard", "Challenge"]
    difficulty = difficulty_names[diff_pos]

    return f"""//--------------- dance-single -  ----------------
    #NOTEDATA:;
    #STEPSTYPE:dance-single;
    #DESCRIPTION:;
    #DIFFICULTY:{difficulty};
    #METER:{chart_rating};
    #RADARVALUES:0,0,0,0,0;
    #NOTES:
    {loadTxt(chart_filepath)}
    ;"""

def loadTxt(chart_filepath: str):
    with open(chart_filepath, 'r') as f:
        return f.read()
    
def pathIsValid(filepath: str):
    try:
        open(filepath, 'w')
    except
    # Finish later