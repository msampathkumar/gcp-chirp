import os
from google.cloud import texttospeech
from typing import List, Optional

class ChirpTTS:
    def __init__(self, credentials_path: Optional[str] = None):
        if credentials_path:
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
        self.client = texttospeech.TextToSpeechClient()

    def list_voices(self, language_code: str = "en-US") -> List[str]:
        """Lists available Chirp 3 HD voices for a specific language."""
        voices = self.client.list_voices(language_code=language_code).voices
        chirp_voices = [
            voice.name for voice in voices 
            if "Chirp3-HD" in voice.name
        ]
        return chirp_voices

    def synthesize(
        self, 
        text: str, 
        voice_name: str = "en-US-Chirp3-HD-A", 
        output_file: str = "output.mp3"
    ) -> str:
        """Synthesizes text using Chirp 3 HD voice."""
        input_text = texttospeech.SynthesisInput(text=text)
        
        # Note: Chirp 3 HD voices are selected via name
        voice = texttospeech.VoiceSelectionParams(
            language_code="-".join(voice_name.split("-")[:2]),
            name=voice_name
        )

        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        response = self.client.synthesize_speech(
            input=input_text, voice=voice, audio_config=audio_config
        )

        with open(output_file, "wb") as out:
            out.write(response.audio_content)
        
        return output_file
