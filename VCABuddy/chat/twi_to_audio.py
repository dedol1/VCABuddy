from datetime import datetime
from django.conf import settings
from TTS.api import TTS
import os


def convert_to_audio():

    api = TTS("tts_models/multilingual/multi-dataset/xtts_v1").to("cuda")



    api.tts_with_vc_to_file(
        "Hello I am going to school",
        speaker_wav="/Users/m1macbookpro2020/Desktop/samuel/final year project/VCABuddy/chat/response.mp3",
        language=api.languages[0],
        file_path="ouptut.wav"
    )


convert_to_audio()