# utils/tts_engine.py

def synthesize_to_memory(text: str, model_path: str) -> bytes:
    from utils.tts_inference import TTSInferenceEngine
    from pydub import AudioSegment

    tts = TTSInferenceEngine(model_path)
    wav_array = tts.infer(text)

    buffer = BytesIO()
    audio = AudioSegment(
        wav_array.tobytes(),
        frame_rate=22050,
        sample_width=2,
        channels=1
    )
    audio.export(buffer, format="ipod")
    buffer.seek(0)
    return buffer.read()
