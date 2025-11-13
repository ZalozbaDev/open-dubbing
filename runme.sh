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

# voice names: weronika korla multi_2025_02_11/VCTK_old_16 michal_multi_2025_02_20 arnd_multi_2025_02_21 katka_2025_07    korla2 cyril
# timbres:     weronika korla multi_2025_02_11             michal_multi_2025_02_20 arnd_multi_2025_02_21 katka_2025_07(*) korla2 cyril daniel(*) jan

# for timbres with (*):
# emotions: neutral happy excited sad angry frightened screaming whispering 


# you need a running "sotra_lmu_fairseq" container, and specify it's "translate" endpoint below
# you need a running "bamborak" backend and specify its API endpoint like below

export SOTRA_URL=http://localhost:3000/translate
# export BAMBORAK_BACKEND=https://bamborakapi.mudrowak.de/api/tts/
export BAMBORAK_BACKEND=http://localhost:8080/api/tts/

if [ "$#" -lt 3 ]; then
	echo "Error! Need to specify 3 args: file, hf token, outdir!"
	exit 1
fi

export FILENAME=$1
export HF_TOKEN=$2
export OUTDIR=$3

echo "Filename=$FILENAME"
echo "HF_TOKEN=$HF_TOKEN"
echo "Output=$OUTDIR"

# enable if updating only!
# export UPDATE="--update"

DEVICE="cpu"
# DEVICE="cuda"

if [ "$#" -gt 3 ]; then
	export SUBSFILE=$4
	echo "Subtitles=$SUBSFILE"

	open-dubbing --input_file $FILENAME --source_language deu --target_language hsb \
	--hugging_face_token $HF_TOKEN --output_directory $OUTDIR \
	--translator sotra --apertium_server $SOTRA_URL \
	--tts bamborak --tts_api_server $BAMBORAK_BACKEND \
	--dubbed_subtitles --original_subtitles --log_level DEBUG --input_srt $SUBSFILE \
	--device $DEVICE $UPDATE

else
	
	open-dubbing --input_file $FILENAME --source_language deu --target_language hsb \
	--hugging_face_token $HF_TOKEN --output_directory $OUTDIR \
	--translator sotra --apertium_server $SOTRA_URL \
	--tts bamborak --tts_api_server $BAMBORAK_BACKEND \
	--dubbed_subtitles --original_subtitles --log_level DEBUG \
	--device $DEVICE $UPDATE
	
fi

# Testing

# 1.: no .srt at all
## rm -rf test4recniki/ && ./runme.sh ~/uploader-recny-model/test/dubbing/4recniki.mp4 HF_TOKEN test4recniki/ 
##
## this shall work and return everything automatically processed

# 2.: with .srt but no speaker info
## rm -rf test4recniki/ && ./runme.sh ~/uploader-recny-model/test/dubbing/4recniki.mp4 HF_TOKEN test4recniki/ ~/uploader-recny-model/test/dubbing/4_recniki.de.srt
##
## this shall fail (not yet supported scenario)

# 3.: with .srt that contains speaker info but no speaker assignments
## rm -rf test4recniki/ && ./runme.sh ~/uploader-recny-model/test/dubbing/4recniki.mp4 HF_TOKEN test4recniki/ ~/uploader-recny-model/test/dubbing/4_recniki.de.speakers.srt
##
## this shall work and create a result as expected

# 4.: with .srt that contains speaker info but no speaker assignments
## rm -rf test4recniki/ && ./runme.sh ~/uploader-recny-model/test/dubbing/4recniki.mp4 HF_TOKEN test4recniki/ ~/uploader-recny-model/test/dubbing/4_recniki.de.speakers.assigned.srt
##
## this shall work and create a result as expected





