SONG_NAME=bxxk2me
ONSET_METHODS=(default hfc)

for onset_method in "${ONSET_METHODS[@]}"; do
	python autostep/main.py $SONG_NAME.mp3 tests/$SONG_NAME/$SONG_NAME-$onset_method.ssc \
		--bpm 148 \
		--offset -0.055 \
		--onset_method $onset_method
done
