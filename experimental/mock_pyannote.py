import pysrt
import re

def extract_utterance_metadata(srt_path):
    subs = pysrt.open(srt_path)
    utterance_metadata = []

    for sub in subs:
        match = re.match(r'\[(SPEAKER_\d+)\]:', sub.text.strip())
        if match:
            speaker_id = match.group(1)
            start_seconds = (
                sub.start.hours * 3600 +
                sub.start.minutes * 60 +
                sub.start.seconds +
                sub.start.milliseconds / 1000
            )
            end_seconds = (
                sub.end.hours * 3600 +
                sub.end.minutes * 60 +
                sub.end.seconds +
                sub.end.milliseconds / 1000
            )
            utterance_metadata.append({
                "start": round(start_seconds, 3),
                "end": round(end_seconds, 3),
                "speaker_id": speaker_id
            })

    return utterance_metadata

