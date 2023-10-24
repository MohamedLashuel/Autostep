from imports import *

class SSC:
    def __init__(self, song: song, chart_filepath: str):
        self.attributes = initialAttributes()

        new_attributes = {'music': song.filepath,
                          'bpms': f'0.000={song.bpm}',
                          'offset': song.offset}

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


#VERSION:0.83;
#TITLE:unknown;
#SUBTITLE:;
#ARTIST:;
#TITLETRANSLIT:;
#SUBTITLETRANSLIT:;
#ARTISTTRANSLIT:;
#GENRE:;
#CREDIT:;
#MUSIC:TurnOffTheLights.mp3;
#BANNER:;
#BACKGROUND:;
#CDTITLE:;
#SAMPLESTART:0.000;
#SAMPLELENGTH:0.000;
#SELECTABLE:YES;
#OFFSET:0.000;
#BPMS:0.000=120.000;
#STOPS:;
#BGCHANGES:;
#FGCHANGES:;
