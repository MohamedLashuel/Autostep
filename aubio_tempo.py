from scipy.io import wavfile
import numpy as np
import aubio

sample_rate, audio_data = wavfile.read("drums.wav")
tempo = aubio.tempo()

audio_data = audio_data.astype(np.float32)
audio_data_l = audio_data[:,0]
audio_data_r = audio_data[:,1]

for i in range(0, int(len(audio_data_l) / 512)):
	tempo(audio_data_l[512*i:512*(i+1)])
	tempo(audio_data_r[512*i:512*(i+1)])

print(tempo.get_bpm())
