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
import logging
import urllib
import requests

from open_dubbing.translation import Translation


class TranslationSotra(Translation):

    def load_model(self):
        pass

    def set_server(self, server):
        if not server.endswith("/"):
            server = server + "/"

        self.server = server

    def _do_api_call(self, url, headers, payload):
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        r = response.read().decode("utf-8")
        data = json.loads(r)
        return data["responseData"]

    def _translate_text(
        self, source_language: str, target_language: str, text: str
    ) -> str:
        payload = {'text':text,'source_language':'deu','target_language':'hsb'}
        headers = {'Content-Type':'application/json'}
        translated = self._do_api_call(self.server, headers, payload)
        translated = translated["translation"]
        return translated.rstrip()

    def get_language_pairs(self):
        source = "deu"
        target = "hsb"
        if len(source) != 3 or len(target) != 3:
            logging.warning(
                f"Discarding Apertium language pair: '{source}-{target}'"
            )

        pair = (source, target)
        results = set()
        results.add(pair)

        return results
