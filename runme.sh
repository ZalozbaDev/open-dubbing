#!/bin/bash

# install local version like this 
# pip install . --break-system-packages
# (better to use a local venv in the future)

# export PATH=$PATH:$HOME/.local/bin

export FILENAME=$1
export SUBSFILE=$2
export HF_TOKEN=$3
export OUTDIR=$4

echo "Filename=$FILENAME"
echo "Subtitles=$SUBSFILE"
echo "HF_TOKEN=$HF_TOKEN"
echo "Output=$OUTDIR"

# you need a running "sotra_lmu_fairseq" container, and specify it's "translate" endpoint below
# you need a running "bamborak" backend and specify its API endpoint like below

open-dubbing --input_file $FILENAME --source_language deu --target_language hsb \
--hugging_face_token $HF_TOKEN --output_directory $OUTDIR \
--translator sotra --apertium_server http://localhost:3000/translate \
--tts bamborak --tts_api_server https://bamborakapi.mudrowak.de/api/tts/ \
--dubbed_subtitles --original_subtitles --log_level DEBUG --input_srt $SUBSFILE \
--device cpu



