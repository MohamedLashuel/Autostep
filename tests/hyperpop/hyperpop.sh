function hyperpop {
	python autostep3/main.py hyperpop.mp3 hyperpop-$1-$2.ssc --bpm 137.81 --offset -0.045 --onset-method $1 --sample2note_method $2
}

#ONSET_METHODS=(default complex hfc)
ONSET_METHODS=(default)
SAMPLE2NOTE_METHODS=(default round offset round+offset)

for onset_method in "${ONSET_METHODS[@]}"; do
	for sample2note_method in "${SAMPLE2NOTE_METHODS[@]}"; do
		hyperpop $onset_method $sample2note_method
	done
done
