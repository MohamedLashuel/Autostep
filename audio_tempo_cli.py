import subprocess

tempo = float(subprocess.check_output("aubio tempo drums.wav", shell=True, text=True).replace(" bpm", ""))

print(tempo)


