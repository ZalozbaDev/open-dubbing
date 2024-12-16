#!/bin/bash

export FILENAME=$1
export HF_TOKEN=$2
export OUTDIR=$3

echo "Filename=$FILENAME"
echo "HF_TOKEN=$HF_TOKEN"
echo "Output=$OUTDIR"

open-dubbing --input_file $FILENAME --source_language deu --target_language hsb \
--hugging_face_token $HF_TOKEN --output_directory $OUTDIR \
--translator sotra --apertium_server http://172.26.0.3:3000/translate \
--tts bamborak --tts_api_server https://bamborakapi.mudrowak.de/api/tts/ \
--dubbed_subtitles



