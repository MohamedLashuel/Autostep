ONSET_METHODS=(default hfc)

for onset_method in "${ONSET_METHODS[@]}"; do
	python autostep/main.py obsessed.mp3 tests/obsessed/obsessed-$onset_method.ssc \
		--bpm 137.81 \
		--offset -0.045 \
		--onset_method $onset_method
done
