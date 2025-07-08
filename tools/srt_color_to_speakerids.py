import pysrt
import re
from datetime import timedelta
import sys

# Check if exactly 2 arguments are provided (excluding the script name)
if len(sys.argv) != 3:
    print("Usage: python srt_color_to_speakerids.py <input_srt> <output_srt>")
    sys.exit(1)

# Get arguments
input_srt = sys.argv[1]
output_srt = sys.argv[2]


# Pattern to extract font color and text
FONT_TAG_RE = re.compile(r'<font color="(#\w{6})">(.*?)</font>', re.DOTALL)

# Map each color to a unique speaker
color_to_speaker = {}
next_speaker_id = 1

def get_speaker_id(color):
    global next_speaker_id
    if color not in color_to_speaker:
        color_to_speaker[color] = f"SPEAKER_{next_speaker_id:02}"
        next_speaker_id += 1
    return color_to_speaker[color]

def datetime_to_timedelta(dt):
    return timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second, milliseconds=dt.microsecond // 1000)

def timedelta_to_subriptime(td):
    total_seconds = int(td.total_seconds())
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return pysrt.SubRipTime(hours=hours, minutes=minutes, seconds=seconds, milliseconds=milliseconds)

def split_sub_by_speaker(sub):
    entries = FONT_TAG_RE.findall(sub.text)
    if not entries:
        return []

    # First, merge blocks of the same speaker *within the same subtitle item*
    merged_by_speaker = []
    last_color = None
    buffer_text = ""
    for color, text in entries:
        if color == last_color:
            buffer_text += " " + text.strip()
        else:
            if last_color is not None:
                merged_by_speaker.append((last_color, buffer_text.strip()))
            last_color = color
            buffer_text = text.strip()
    if last_color is not None:
        merged_by_speaker.append((last_color, buffer_text.strip()))

    total_chars = sum(len(text) for _, text in merged_by_speaker)
    start_time = datetime_to_timedelta(sub.start.to_time())
    end_time = datetime_to_timedelta(sub.end.to_time())
    total_duration = (end_time - start_time).total_seconds()

    current_time = start_time
    results = []

    for color, text in merged_by_speaker:
        duration = total_duration * len(text) / total_chars if total_chars > 0 else 0
        delta = timedelta(seconds=duration)
        speaker = get_speaker_id(color)

        new_sub = pysrt.SubRipItem()
        new_sub.start = timedelta_to_subriptime(current_time)
        new_sub.end = timedelta_to_subriptime(current_time + delta)
        new_sub.text = f"[{speaker}]: {text}"

        results.append(new_sub)
        current_time += delta

    return results

def process_srt(input_path, output_path):
    subs = pysrt.open(input_path)
    new_subs = []

    for sub in subs:
        split_subs = split_sub_by_speaker(sub)
        for new_sub in split_subs:
            new_sub.index = len(new_subs) + 1
            new_subs.append(new_sub)

    srt_file = pysrt.SubRipFile(items=new_subs)
    srt_file.save(output_path, encoding='utf-8')

# Example usage
process_srt(input_srt, output_srt)
