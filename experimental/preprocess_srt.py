import pysrt
import re
from collections import defaultdict
from datetime import timedelta

# Pattern to extract font color and text
FONT_TAG_RE = re.compile(r'<font color="(#\w{6})">(.*?)</font>', re.DOTALL)

# Mapping font colors to speaker IDs
color_to_speaker = {}
next_speaker_id = 1

def get_speaker_id(color):
    global next_speaker_id
    if color not in color_to_speaker:
        color_to_speaker[color] = f"SPEAKER_{next_speaker_id:02}"
        next_speaker_id += 1
    return color_to_speaker[color]

def split_sub_by_speaker(sub):
    entries = FONT_TAG_RE.findall(sub.text)
    if not entries:
        return []

    total_chars = sum(len(text) for _, text in entries)
    start_time = sub.start.to_time()
    end_time = sub.end.to_time()
    total_duration = (datetime_to_timedelta(end_time) - datetime_to_timedelta(start_time)).total_seconds()

    results = []
    current_time = datetime_to_timedelta(start_time)

    for color, text in entries:
        duration = total_duration * len(text) / total_chars if total_chars > 0 else 0
        delta = timedelta(seconds=duration)
        speaker = get_speaker_id(color)

        new_sub = pysrt.SubRipItem()
        new_sub.start = pysrt.SubRipTime.from_ordinal(int(current_time.total_seconds() * 1000))
        new_sub.end = pysrt.SubRipTime.from_ordinal(int((current_time + delta).total_seconds() * 1000))
        new_sub.text = f"[{speaker}]: {text.strip()}"

        results.append(new_sub)
        current_time += delta

    return results

def datetime_to_timedelta(dt):
    return timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second, milliseconds=dt.microsecond // 1000)

def merge_consecutive_speakers(subs):
    if not subs:
        return []
    merged = [subs[0]]

    for sub in subs[1:]:
        last = merged[-1]
        current_speaker = re.match(r'\[(SPEAKER_\d{2})\]:', sub.text)
        last_speaker = re.match(r'\[(SPEAKER_\d{2})\]:', last.text)

        if current_speaker and last_speaker and current_speaker.group(1) == last_speaker.group(1):
            # Merge texts and adjust end time
            last.text += " " + re.sub(r'^\[SPEAKER_\d{2}\]:\s*', '', sub.text)
            last.end = sub.end
        else:
            merged.append(sub)

    return merged

def process_srt(input_path, output_path):
    subs = pysrt.open(input_path)
    new_subs = []

    for sub in subs:
        split_subs = split_sub_by_speaker(sub)
        new_subs.extend(split_subs)

    merged_subs = merge_consecutive_speakers(new_subs)

    # Reassign indices
    for i, sub in enumerate(merged_subs, start=1):
        sub.index = i

    srt_file = pysrt.SubRipFile(items=merged_subs)
    srt_file.save(output_path, encoding='utf-8')

# Example usage
process_srt('../../kick_it/kick_it.srt', './kick_proc.srt')
