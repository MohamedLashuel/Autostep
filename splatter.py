# Test a song with every method at once
# Usage: python splatter.py {song path}

from tests import *
from autostep import better_aubio
import os

assert len(sys.argv) == 2

if not os.path.exists('splatter'): os.mkdir('splatter')

for method in better_aubio.ONSET_METHODS:
    runProg(f'{sys.argv[1]} --output_dir splatter/{method} --onset_method {method} --overwrite --division 64')
