#!/bin/bash

# install local version like this 
# pip install . --break-system-packages

# better to use a local venv:
#   python3 -m venv .
#   source bin/activate

# export PATH=$PATH:$HOME/.local/bin

#######################
# convert colored .srt files like this:
#
# python3.12 tools/srt_color_to_speakerids.py harald_lesch/harald_lesch.srt harald_lesch/harald_lesch_good.srt
# 
#######################


##### format for specifying speakers
#
# 1
# 00:00:00,000 --> 00:00:00,000
# [SPEAKER_01]: cyril,Male
# 




# you need a running "sotra_lmu_fairseq" container, and specify it's "translate" endpoint below
# you need a running "bamborak" backend and specify its API endpoint like below

export SOTRA_URL=http://localhost:3000/translate
# export BAMBORAK_BACKEND=https://bamborakapi.mudrowak.de/api/tts/
export BAMBORAK_BACKEND=http://localhost:8080/api/tts/


export FILENAME=$1
export SUBSFILE=$2
export HF_TOKEN=$3
export OUTDIR=$4

echo "Filename=$FILENAME"
echo "Subtitles=$SUBSFILE"
echo "HF_TOKEN=$HF_TOKEN"
echo "Output=$OUTDIR"

# enable if updating only!
# export UPDATE="--update"

open-dubbing --input_file $FILENAME --source_language deu --target_language hsb \
--hugging_face_token $HF_TOKEN --output_directory $OUTDIR \
--translator sotra --apertium_server $SOTRA_URL \
--tts bamborak --tts_api_server $BAMBORAK_BACKEND \
--dubbed_subtitles --original_subtitles --log_level DEBUG --input_srt $SUBSFILE \
--device cpu $UPDATE



