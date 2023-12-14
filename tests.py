# In order to run tests, just do python tests.py from the project directory (the same directory this file is in)

import os, sys, shutil

import sys
sys.path.append('/autostep')
from autostep import main

def runProg(args):
    sys.argv[1:] = args.split(' ')
    main.main()

def tryDelete(*paths):
    def tryDeleteOne(path):
        if not os.path.exists(path): return
        try:
            os.remove(path)
        except IsADirectoryError:
            shutil.rmtree(path)

    for path in paths: tryDeleteOne(path)

# Setup
tryDelete('chart.txt', 'code.txt', 'TOTL.ogg, TOTL.ssc')

# With and without separation
tryDelete('TOTL', 'TOTL2')

if os.path.exists('separated/TOTL'):
    shutil.rmtree('separated/TOTL')
runProg('test_audio/TOTL.ogg --output_dir TOTL')

runProg('test_audio/TOTL.ogg --output_dir TOTL2')

# Forcing
try:
    runProg('test_audio/TOTL.ogg --output_dir TOTL')
# If we don't force, program should quit() with code 1
except SystemExit as e:
    assert e.code == 1 

try:
    runProg('test_audio/TOTL.ogg --output_dir TOTL --force')
except SystemExit as e:
    raise Exception('Forced folder overwrite failed to run')

# Output dir here
runProg('test_audio/TOTL.ogg')