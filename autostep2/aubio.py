def aubioPeaks(song: Song, fft: int, hop: int, mode: int) -> np.ndarray:
	if mode <= 0 or mode > 8:
		algorithm = 'default'
	else:
		algorithm = {
			1: 'complex',
			2: 'energy',
			3: 'phase',
			4: 'specdiff',
			5: 'specflux',
			6: 'kl',
			7: 'mkl',
			8: 'hfc'
		}[mode]

	# We can't use the existing song data for this
	s = aubio.source(song.filepath, song.samplerate, hop)
	o = aubio.onset(algorithm, fft, hop, song.samplerate)

	onsets = []
	num_read = hop
	while num_read >= hop:
		samples, num_read = s()
		if o(samples):
			onsets.append(o.get_last())

	return np.int32(onsets)
