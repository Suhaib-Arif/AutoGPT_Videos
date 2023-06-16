import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s ==> at line %(lineno)d --> %(message)s", datefmt="%m-%d "
                                                                                                             "%H:%M:%S")

import requests
from assetsmanager import AssetHandler



import sys

class Voiceover:

    def __init__(self,ELEVENLABS_VOICE_ID, ELEVENLABSAPIKEY):
        self.handler = AssetHandler()
        self.audio_dir = self.handler.audio_dir
        self.ELEVENLABS_VOICE_ID = ELEVENLABS_VOICE_ID
        self.ELEVENLABSAPIKEY = ELEVENLABSAPIKEY
        self.url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.ELEVENLABS_VOICE_ID}"

        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.ELEVENLABSAPIKEY
        }

    def obtain_audio(self,text,index):

        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5
            }
        }

        logging.info("Requesting Voice-Over from ElevenLabs")

        audio_response = requests.post(self.url, json=data, headers=self.headers)

        logging.info(f"Request Status Code: {audio_response.status_code}")

        if audio_response.status_code == 200:

            audio_file_name = f"{index}audio.mp3"

            audio_file_dir = self.handler.combine_directory(self.audio_dir, audio_file_name)

            with open(audio_file_dir, 'wb') as f:
                for chunk in audio_response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            saved_file = self.handler.get_latest_file(self.audio_dir)

            logging.info(f"audio file saved locally --> {saved_file} ")

            return audio_file_dir

        else:

            error_message = audio_response.json()['detail']["message"]
            logging.error(error_message)
            sys.exit()

