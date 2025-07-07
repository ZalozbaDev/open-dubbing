from mock_whisper import find_texts_by_time

metadata_list = [
    {'start': 102.4, 'end': 104.799, 'speaker_id': 'SPEAKER_01'},
    {'start': 104.92, 'end': 107.76, 'speaker_id': 'SPEAKER_01'},
    {'start': 107.879, 'end': 110.159, 'speaker_id': 'SPEAKER_01'},
    {'start': 110.28, 'end': 111.48, 'speaker_id': 'SPEAKER_01'},
    {'start': 111.599, 'end': 114.28, 'speaker_id': 'SPEAKER_01'},
    {'start': 114.4, 'end': 117.28, 'speaker_id': 'SPEAKER_01'},
    {'start': 114.4, 'end': 119.28, 'speaker_id': 'SPEAKER_01'}  # ← this one doesn't match

]

results = find_texts_by_time("kick_proc.srt", metadata_list)

for text in results:
    print(text)
