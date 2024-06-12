import torch
import torchaudio
import torch_xla.core.xla_model as xm
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor

# Load the processor and model
processor = Wav2Vec2Processor.from_pretrained("facebook/wav2vec2-base-960h")
model = Wav2Vec2ForCTC.from_pretrained("facebook/wav2vec2-base-960h").to(xm.xla_device())

def transcribe_audio_tpu(audio_file):
    waveform, sample_rate = torchaudio.load(audio_file)
    input_values = processor(waveform, return_tensors="pt", sampling_rate=sample_rate).input_values.to(xm.xla_device())
    with torch.no_grad():
        logits = model(input_values).logits
    transcription = processor.batch_decode(torch.argmax(logits, dim=-1))
    return transcription[0]
