function error_and_exit {
	echo ERROR: $1
	exit 1
}

SONG_NAME=$1
TEST_DIR=tests/$SONG_NAME

[ ! -d $TEST_DIR ] && error_and_exit Directory $TEST_DIR does not exist.

TEST_PATH=$TEST_DIR/$SONG_NAME

[ ! -e "$TEST_PATH.sh" ] && error_and_exit $TEST_PATH.sh does not exist.

source $TEST_PATH.sh

[ -z $BPM ] && error_and_exit $TEST_PATH.sh did not set BPM.

[ -z $OFFSET ] && error_and_exit $TEST_PATH.sh did not set OFFSET.

[ -z $EXT ] && error_and_exit $TEST_PATH.sh did not set EXT.

[ ! -e "$TEST_PATH.$EXT" ] && error_and_exit $TEST_PATH.$EXT does not exist.

[ -z $ONSET_METHODS ] && error_and_exit $TEST_PATH.sh did not set ONSET_METHODS.

[ -z $SAMPLE2NOTE_METHODS ] && error_and_exit $TEST_PATH.sh did not set SAMPLE2NOTE_METHODS.

for onset_method in "${ONSET_METHODS[@]}"; do
	for sample2note_method in "${SAMPLE2NOTE_METHODS[@]}"; do
		python autostep/main.py $TEST_PATH.$EXT $TEST_PATH-$onset_method-$sample2note_method.ssc \
			--bpm $BPM \
			--offset $OFFSET \
			--onset_method $onset_method \
			--sample2note_method $sample2note_method
	done
done
