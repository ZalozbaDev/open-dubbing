# Copyright 2024 Jordi Mas i Hernàndez <jmas@softcatala.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import tempfile

from open_dubbing.preprocessing import PreprocessingArtifacts
from open_dubbing.utterance import Utterance


class TestUtterance:

    def testrun_save_utterance(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = temp_dir

            utterance = Utterance(
                target_language="cat",
                output_directory=directory,
            )
            utterance_metadata = [
                {"start": 1.26, "end": 3.94},
                {"start": 5.24, "end": 6.629},
            ]

            utterance.save_utterances(
                metadata={"source_language": "spa"},
                utterance_metadata=utterance_metadata,
                preprocessing_output=None,
            )
            metadata_file = os.path.join(directory, "utterance_metadata_cat.json")
            with open(metadata_file, encoding="utf-8") as json_data:
                data = json.load(json_data)
                assert data == {
                    "utterances": [
                        {
                            "id": 1,
                            "start": 1.26,
                            "end": 3.94,
                            "_hash": "26d514d9ce21021f51bd010d9946db0f31555ef7145067d4fe5a3b1bdcd84ce7",
                        },
                        {
                            "id": 2,
                            "start": 5.24,
                            "end": 6.629,
                            "_hash": "157dc7fb355c7dc13a0ea687e9fd4a6f6c5c03526a959a64dfe1fa7562fedff4",
                        },
                    ],
                    "metadata": {
                        "source_language": "spa",
                    },
                }

    def test_hash_utterances(self):
        utterances = [
            {
                "start": 1.26,
                "end": 3.94,
                "_private_not_hashed": "0",
            },
            {
                "start": 5.24,
                "end": 6.629,
            },
        ]
        utterance = Utterance(
            target_language="cat",
            output_directory=None,
        )

        hashed = utterance._hash_utterances(utterances)
        assert hashed == [
            {
                "start": 1.26,
                "end": 3.94,
                "_private_not_hashed": "0",
                "_hash": "2fa6f80e0c81fb8e142f2dbbad0bceff7c21a031833b5752bc1cfd799f6b3bc6",
            },
            {
                "start": 5.24,
                "end": 6.629,
                "_hash": "34cd5da78cb163ad18996aefffcfeae864727257defc7ae68818a245ca269951",
            },
        ]

    def test_get_modified_utterances(self):
        utterances = [
            {
                "id": 1,
                "start": 1.26,
                "end": 3.94,
                "_hash": "26d514d9ce21021f51bd010d9946db0f31555ef7145067d4fe5a3b1bdcd84ce7",
            },
            {
                "id": 2,
                "start": 5.25,
                "end": 6.629,
                "_hash": "157dc7fb355c7dc13a0ea687e9fd4a6f6c5c03526a959a64dfe1fa7562fedff4",
            },
        ]
        dubbing = Utterance(
            target_language="cat",
            output_directory=None,
        )

        modified = dubbing.get_modified_utterances(utterances)
        assert 1 == len(modified)
        assert 2 == modified[0]["id"]

    def test_get_without_empty_blocks(self):
        utterances = [
            {
                "start": 1.26,
                "end": 3.94,
                "text": "Hola",
            },
            {
                "start": 5.24,
                "end": 6.600,
                "text": "",
            },
        ]

        dubbing = Utterance(
            target_language="cat",
            output_directory=None,
        )

        modified = dubbing.get_without_empty_blocks(utterances)
        assert 1 == len(modified)
        assert "Hola" == modified[0]["text"]

    def test_add_unique_ids(self):
        utterances = [
            {
                "start": 1.26,
                "end": 3.94,
            },
            {
                "start": 5.24,
                "end": 6.629,
            },
        ]
        utterance = Utterance(
            target_language="cat",
            output_directory=None,
        )

        unique_ids = utterance._add_unique_ids(utterances)
        assert unique_ids == [
            {"id": 1, "start": 1.26, "end": 3.94},
            {"id": 2, "start": 5.24, "end": 6.629},
        ]

    def _get_master_utterances(self):
        return [
            {
                "id": 1,
                "start": 1.26284375,
                "end": 3.94596875,
                "speaker_id": "SPEAKER_00",
                "path": "output/jordi.central.edge.update/chunk_1.26284375_3.94596875.mp3",
                "text": "Good morning, my name is Jordi Mas.",
                "for_dubbing": True,
                "gender": "Male",
                "translated_text": "Bon dia, el meu nom és Jordi Mas.",
                "assigned_voice": "ca-ES-EnricNeural",
                "speed": 1.0,
                "dubbed_path": "output/jordi.central.edge.update/dubbed_chunk_1.26284375_3.94596875.mp3",
                "_hash": "b01b399ac50f80f87e704918e290ffc5ee0a1962683ba946c627124ea903480d",
            },
            {
                "id": 2,
                "start": 5.24534375,
                "end": 6.629093750000001,
                "speaker_id": "SPEAKER_00",
                "path": "output/jordi.central.edge.update/chunk_5.24534375_6.629093750000001.mp3",
                "text": "I am from Barcelona.",
                "for_dubbing": True,
                "gender": "Male",
                "translated_text": "Sóc de Barcelona.",
                "assigned_voice": "ca-ES-EnricNeural",
                "speed": 1.0,
                "dubbed_path": "output/jordi.central.edge.update/dubbed_chunk_5.24534375_6.629093750000001.mp3",
                "_hash": "629484afdecb7641e35d686d6348cee4445611690f2f77831e892d52c3128bdd",
            },
        ]

    def test_update_utterances_operation_create(self):
        master = self._get_master_utterances()
        utterance = Utterance(
            target_language="cat",
            output_directory=None,
        )
        create_utterances = [
            {
                "id": 1,
                "operation": "create",
                "translated_text": "Bon dia",
                "speaker_id": "SPEAKER_01",
                "gender": "Male",
                "assigned_voice": "ca-ES-EnricNeural",
                "start": 4,
                "end": 5,
            }
        ]
        new_utterances = utterance.update_utterances(master, create_utterances)
        assert len(new_utterances) == 3
        assert [u["id"] for u in new_utterances] == [1, 3, 2]
        assert new_utterances[1]["translated_text"] == "Bon dia"

    def test_update_utterances_operation_create_first(self):
        master = self._get_master_utterances()
        utterance = Utterance(
            target_language="cat",
            output_directory=None,
        )
        create_utterances = [
            {
                "id": 0,
                "operation": "create",
                "translated_text": "Bon dia",
                "speaker_id": "SPEAKER_01",
                "gender": "Male",
                "assigned_voice": "ca-ES-EnricNeural",
                "start": 4,
                "end": 5,
            }
        ]
        new_utterances = utterance.update_utterances(master, create_utterances)
        assert len(new_utterances) == 3
        assert [u["id"] for u in new_utterances] == [3, 1, 2]
        assert new_utterances[0]["translated_text"] == "Bon dia"

    def test_update_utterances_operation_create_ignore_missing_fields(self):
        master = self._get_master_utterances()
        utterance = Utterance(
            target_language="cat",
            output_directory=None,
        )
        create_utterances = [
            {
                "id": 0,
                "operation": "create",
                "gender": "Male",
                "assigned_voice": "ca-ES-EnricNeural",
                "start": 4,
                "end": 5,
            }
        ]
        new_utterances = utterance.update_utterances(master, create_utterances)
        assert len(new_utterances) == 2
        assert [u["id"] for u in new_utterances] == [1, 2]

    def test_update_utterances_operation_delete(self):
        master = self._get_master_utterances()
        utterance = Utterance(
            target_language="cat",
            output_directory=None,
        )

        update_utterances = [{"id": 1, "operation": "delete"}]
        new_utterances = utterance.update_utterances(master, update_utterances)
        assert len(new_utterances) == 1
        assert new_utterances[0]["id"] == 2

    def test_update_utterances_operation_update(self):
        master = self._get_master_utterances()
        utterance = Utterance(
            target_language="cat",
            output_directory=None,
        )

        update_utterances = [
            {
                "id": 2,
                "operation": "update",
                "gender": "Female",
                "translated_text": "Sóc de Tarragona",
            }
        ]
        new_utterances = utterance.update_utterances(master, update_utterances)
        assert len(new_utterances) == 2
        assert new_utterances[0] == master[0]
        assert new_utterances[1] == {
            "id": 2,
            "start": 5.24534375,
            "end": 6.629093750000001,
            "speaker_id": "SPEAKER_00",
            "path": "output/jordi.central.edge.update/chunk_5.24534375_6.629093750000001.mp3",
            "text": "I am from Barcelona.",
            "for_dubbing": True,
            "gender": "Female",
            "translated_text": "Sóc de Tarragona",
            "assigned_voice": "ca-ES-EnricNeural",
            "speed": 1.0,
            "dubbed_path": "output/jordi.central.edge.update/dubbed_chunk_5.24534375_6.629093750000001.mp3",
            "_hash": "629484afdecb7641e35d686d6348cee4445611690f2f77831e892d52c3128bdd",
        }

    def test_load_utterances(self):
        directory = os.path.dirname(os.path.realpath(__file__))
        directory = os.path.join(directory, "data/")
        utterance = Utterance(target_language="cat", output_directory=directory)

        utterances, preprocessing_output, metadata = utterance.load_utterances()
        assert utterances == [{"id": 1, "text": "Good morning."}]

        assert preprocessing_output == PreprocessingArtifacts(
            video_file="jordi_video.mp4",
            audio_file="jordi_audio.mp3",
            audio_vocals_file="htdemucs/jordi_audio/vocals.mp3",
            audio_background_file="htdemucs/jordi_audio/no_vocals.mp3",
        )

        assert metadata == {
            "source_language": "eng",
            "original_subtitles": False,
            "dubbed_subtitles": False,
        }

    def _get_utterance(self):
        return {
            "id": 2,
            "start": 5.24534375,
            "end": 6.64596875,
            "speaker_id": "SPEAKER_00",
            "path": "output/jordi.voices/chunk_5.24534375_6.64596875.mp3",
            "text": "I am from Barcelona.",
            "for_dubbing": "true",
            "gender": "Male",
            "translated_text": "Soc de Barcelona.",
            "assigned_voice": "2",
            "speed": 1.0,
            "dubbed_path": "output/jordi.voices/dubbed_chunk_5.24534375_6.64596875.mp3",
            "_hash": "ea1d02c92026bc8cd6144a6500489333bdf0b58368817ea5116189d101c1fe9e",
            "_assigned_voice_hash": "d4735e3a265e16eee03f59718b9b5d03019c07d8b6c51f90da3a666eec13ab35",
            "_speaker_id_hash": "bf4f81ea701e475a4268bb9f36ddb43d7d5c0dbf4578fd5a24c3a8b5a375b4c9",
        }

    def test_get_modified_utterances_with_field_hashes(self):
        utterances = [self._get_utterance()]
        dubbing = Utterance(
            target_language="cat",
            output_directory=None,
        )

        modified = dubbing.get_modified_utterances(utterances)
        assert 0 == len(modified)

    def test_get_modified_utterance_fields_none(self):
        utterance = self._get_utterance()
        u = Utterance(target_language="cat", output_directory="")
        fields = u.get_modified_utterance_fields(utterance)
        assert len(fields) == 0

    def test_get_modified_utterance_fields_speaker_id(self):
        utterance = self._get_utterance()
        utterance["speaker_id"] = "SPEAKER_01"
        u = Utterance(target_language="cat", output_directory="")
        fields = u.get_modified_utterance_fields(utterance)
        assert len(fields) == 1
        assert "speaker_id" == fields[0]
