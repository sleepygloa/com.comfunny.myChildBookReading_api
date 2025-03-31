import onnxruntime as ort
import numpy as np
from pydub import AudioSegment

class TTSInferenceEngine:
    def __init__(self, model_path: str):
        self.session = ort.InferenceSession(model_path)
        self.input_name = self.session.get_inputs()[0].name
        self.output_name = self.session.get_outputs()[0].name

    def infer(self, text: str) -> np.ndarray:
        print(f"[TTS] '{text}' → 음성 추론")
        # ⚠️ 아래는 임시: 실제로는 텍스트를 토크나이즈하고 벡터로 변환해야 함
        fake_input = np.random.rand(1, 100).astype(np.float32)
        result = self.session.run([self.output_name], {self.input_name: fake_input})
        return result[0].squeeze().astype(np.int16)

def save_audio_to_m4a(wav_array: np.ndarray, output_path: str):
    audio = AudioSegment(
        wav_array.tobytes(),
        frame_rate=22050,
        sample_width=2,
        channels=1
    )
    audio.export(output_path, format="ipod")
