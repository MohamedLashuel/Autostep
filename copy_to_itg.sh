ITG_SONG_PATH=~/.itgmania/Songs/Autostep/$1

# create a directory for the song
mkdir -p $ITG_SONG_PATH

# copy the ssc
cp $1.ssc $ITG_SONG_PATH

# copy the audio
cp test_audio/$1.mp3 $ITG_SONG_PATH
