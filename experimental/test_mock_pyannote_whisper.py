from mock_pyannote import extract_utterance_metadata
from mock_whisper import find_texts_by_time

metadata = extract_utterance_metadata("kick_proc.srt")
for item in metadata:
    print(item)

results = find_texts_by_time("kick_proc.srt", metadata)

for text in results:
    print(text)
