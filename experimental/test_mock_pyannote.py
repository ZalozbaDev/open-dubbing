from mock_pyannote import extract_utterance_metadata

metadata = extract_utterance_metadata("kick_proc.srt")
for item in metadata:
    print(item)
