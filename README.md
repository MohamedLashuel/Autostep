# Autostep
A Python program that turns music into StepMania/ITGmania charts.

## Installation
```sh
pip install autostep
```

## Getting started with development
To setup a devlopment environment for Autostep, run:
```sh
git clone https://github.com/MohamedLashuel/Autostep
cd Autostep
sh scripts/devsetup.sh
```

## Building
To build Autostep into an installable `.whl` file, run this command in the current directory:
```sh
python -m build
```

To install the built package into your local Python environment, run:
```sh
pip install dist/*.whl
```

## Dependencies
- [nathanstep55/bpm-offset-detector](https://github.com/nathanstep55/bpm-offset-detector)
- [aubio/aubio](https://github.com/aubio/aubio)
- [deezer/spleeter](https://github.com/deezer/spleeter)
- [bastibe/python-soundfile](https://github.com/bastibe/python-soundfile)
- [numpy/numpy](https://github.com/numpy/numpy)
