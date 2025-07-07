import pysrt
import re

def find_texts_by_time(srt_path, metadata_list, time_tolerance=0.05):
    """
    Given a list of subtitle metadata and an SRT file, returns the corresponding
    subtitle texts (without speaker labels), matching by start/end time with a small tolerance.
    
    If a match is not found, prints a warning and returns an empty string in that slot.

    :param srt_path: Path to the .srt file
    :param metadata_list: List of dicts with 'start', 'end', 'speaker_id'
    :param time_tolerance: Time in seconds to allow as matching margin (default: 0.05s)
    :return: List of strings (subtitle texts without speaker labels)
    """
    subs = pysrt.open(srt_path)
    matched_texts = []

    def time_to_seconds(t):
        return t.hours * 3600 + t.minutes * 60 + t.seconds + t.milliseconds / 1000.0

    for meta in metadata_list:
        target_start = meta['start']
        target_end = meta['end']
        match = None

        for sub in subs:
            sub_start = time_to_seconds(sub.start)
            sub_end = time_to_seconds(sub.end)

            if (abs(sub_start - target_start) <= time_tolerance and
                abs(sub_end - target_end) <= time_tolerance):

                # Remove the [SPEAKER_XX]: tag
                clean_text = re.sub(r'^\[SPEAKER_\d{2}\]:\s*', '', sub.text.strip())
                match = clean_text
                break

        if match is None:
            print(f"\n⚠️ WARNING: No subtitle match found for time range {target_start:.3f}–{target_end:.3f} seconds "
                  f"(speaker {meta.get('speaker_id', 'UNKNOWN')})\n")
            matched_texts.append("")
        else:
            matched_texts.append(match)

    return matched_texts
