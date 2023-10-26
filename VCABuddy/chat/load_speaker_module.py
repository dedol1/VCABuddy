import os
from django.conf import settings
from TTS.api import TTS

# Define a function to load the model
def load_speaker_encoder_model_twi():
    model_path = "tts_models/tw_asante/openbible/vits"  # Replace with the actual model path
    return TTS(model_path)

def load_speaker_encoder_model_ewe():
    model_path = "tts_models/ewe/openbible/vits"  # Replace with the actual model path
    return TTS(model_path)

# Load the model during server startup
speaker_encoder_model_twi = load_speaker_encoder_model_twi()
speaker_encoder_model_ewe = load_speaker_encoder_model_ewe()
