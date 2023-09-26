import array2chart
import itertools as it

def readCodeTxt():
    with open('code.txt') as f:
        return f.read()[2:]
    
def optimize(func1, func2, bpm, sample_rate, ranges):
    min_combo = (0,0,0)
    min_score = None

    for combo in it.product(*ranges):
        peaks = func2(*combo)
        array2chart.arrayToChart(peaks, bpm, sample_rate)
        print(combo)
        score = func1()

        if min_score == None or score < min_score: 
            score = min_score
            min_combo = combo

    return min_combo


def thirtysecondtest(quiet = False):
    code = readCodeTxt()
    
    sixteenths = 0
    thirtyseconds = 0

    on_sixteenth = True

    for chr in code:
        if chr == '/': continue
        elif chr == 'n':
            if on_sixteenth: sixteenths += 1
            else: thirtyseconds += 1

        on_sixteenth = not on_sixteenth

    if not quiet:
        print(f'Sixteenths: {sixteenths}')
        print(f'Thirtyseconds: {thirtyseconds}')

    return thirtyseconds

