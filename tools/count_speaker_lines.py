import pysrt
import sys
import re
from collections import defaultdict

def count_speaker_lines(srt_file):
    # Load subtitles
    try:
        subs = pysrt.open(srt_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    speaker_counts = defaultdict(int)
    speaker_pattern = re.compile(r'^\[(.*?)\]:', re.IGNORECASE)

    for sub in subs:
        match = speaker_pattern.match(sub.text.strip())
        if match:
            speaker = match.group(1).strip()
            speaker_counts[speaker] += 1

    if not speaker_counts:
        print("No speaker annotations found in the subtitles.")
    else:
        print("Subtitle count per speaker:")
        for speaker, count in sorted(speaker_counts.items(), key=lambda x: -x[1]):
            print(f"{speaker}: {count}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python count_speaker_lines.py <subtitle_file.srt>")
        sys.exit(1)

    srt_file = sys.argv[1]
    count_speaker_lines(srt_file)
