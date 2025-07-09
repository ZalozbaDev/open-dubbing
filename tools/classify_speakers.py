import pysrt
import sys
import re
from collections import defaultdict, Counter

def extract_speaker(text):
    match = re.match(r'^\[(.*?)\]:', text.strip(), re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return None

def classify_speakers(srt_file):
    try:
        subs = pysrt.open(srt_file)
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)

    speaker_counts = defaultdict(int)
    dialogue_sequence = []

    for sub in subs:
        speaker = extract_speaker(sub.text)
        if speaker:
            speaker_counts[speaker] += 1
            dialogue_sequence.append(speaker)

    print("Subtitle count per speaker:")
    for speaker, count in sorted(speaker_counts.items(), key=lambda x: -x[1]):
        print(f"{speaker}: {count}")

    print("\nTop 3 conversation partners per speaker:")
    top_conversation_partners(dialogue_sequence)

def top_conversation_partners(dialogue_sequence):
    interaction_counts = defaultdict(Counter)

    # Analyze adjacent speaker pairs
    for i in range(1, len(dialogue_sequence)):
        prev_speaker = dialogue_sequence[i - 1]
        curr_speaker = dialogue_sequence[i]
        if prev_speaker != curr_speaker:
            interaction_counts[prev_speaker][curr_speaker] += 1
            interaction_counts[curr_speaker][prev_speaker] += 1

    for speaker, partners in interaction_counts.items():
        top_3 = partners.most_common(3)
        print(f"{speaker}: {[f'{p} ({c})' for p, c in top_3]}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python classify_speakers.py <subtitle_file.srt>")
        sys.exit(1)

    srt_file = sys.argv[1]
    classify_speakers(srt_file)
