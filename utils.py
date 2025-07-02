import torch
import soundfile as sf
import librosa
from transformers import Wav2Vec2Tokenizer, Wav2Vec2ForCTC

# Load the ASR model and tokenizer
speech_tokenizer = Wav2Vec2Tokenizer.from_pretrained("facebook/wav2vec2-base-960h")
speech_model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h")

def format_audio(input_path):
    """Load and resample audio to 16kHz, save as temp file."""
    waveform, _ = librosa.load(input_path, sr=16000)
    temp_path = "converted.wav"
    sf.write(temp_path, waveform, 16000)
    return temp_path

def convert_speech_to_text(wav_path):
    """Transcribe the audio to text using pretrained model."""
    audio_data, _ = sf.read(wav_path)
    encoded_input = speech_tokenizer(audio_data, return_tensors="pt", padding="longest").input_values

    with torch.no_grad():
        logits_output = speech_model(encoded_input).logits

    predicted_ids = torch.argmax(logits_output, dim=-1)
    decoded_text = speech_tokenizer.decode(predicted_ids[0])

    return decoded_text
