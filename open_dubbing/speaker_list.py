import re
from dataclasses import dataclass, field
from typing import List

@dataclass
class Speaker:
    speaker_id: str
    name: str
    gender: str

@dataclass
class SpeakerList:
    speakers: List[Speaker] = field(default_factory=list)

    def is_valid(self) -> bool:
        """Check if there is at least one speaker."""
        return len(self.speakers) > 0

    def add_speaker(self, speaker_id: str, name: str, gender: str):
        """Add a new speaker to the list."""
        self.speakers.append(Speaker(speaker_id, name, gender))
