import pytest
from gcp_chirp.tts import ChirpTTS

def test_synthesize_call_structure(mocker):
    mock_client = mocker.patch("google.cloud.texttospeech.TextToSpeechClient")
    # Mock the return value of synthesize_speech
    mock_response = mocker.Mock()
    mock_response.audio_content = b"fake audio content"
    mock_client.return_value.synthesize_speech.return_value = mock_response
    
    tts = ChirpTTS()
    tts.synthesize("Hello world", voice_name="en-US-Chirp3-HD-Aoede", output_file="test.mp3")
    
    # Verify that synthesize_speech was called
    assert mock_client.return_value.synthesize_speech.called
    
    # Verify input structure
    args, kwargs = mock_client.return_value.synthesize_speech.call_args
    assert kwargs['input'].text == "Hello world"
    assert kwargs['voice'].name == "en-US-Chirp3-HD-Aoede"

def test_list_voices_filtering(mocker):
    mock_client = mocker.patch("google.cloud.texttospeech.TextToSpeechClient")
    
    # Create fake voice response
    class FakeVoice:
        def __init__(self, name):
            self.name = name
            
    mock_client.return_value.list_voices.return_value.voices = [
        FakeVoice("en-US-Standard-A"),
        FakeVoice("en-US-Chirp3-HD-Aoede"),
        FakeVoice("en-US-News-B")
    ]
    
    tts = ChirpTTS()
    voices = tts.list_voices("en-US")
    
    assert len(voices) == 1
    assert voices[0] == "en-US-Chirp3-HD-Aoede"
def test_synthesize_quota_error(mocker):
    mock_client = mocker.patch("google.cloud.texttospeech.TextToSpeechClient")
    mock_client.return_value.synthesize_speech.side_effect = Exception("Quota exceeded for project")
    
    tts = ChirpTTS()
    with pytest.raises(Exception) as excinfo:
        tts.synthesize("Hello")
    assert "API Quota exceeded" in str(excinfo.value)

def test_synthesize_auth_error(mocker):
    mock_client = mocker.patch("google.cloud.texttospeech.TextToSpeechClient")
    mock_client.return_value.synthesize_speech.side_effect = Exception("Invalid credentials")
    
    tts = ChirpTTS()
    with pytest.raises(Exception) as excinfo:
        tts.synthesize("Hello")
    assert "Authentication failed" in str(excinfo.value)
