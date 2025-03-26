# utils/synthesizer.py
import time
import soundfile as sf
import numpy as np

def synthesize_speech(model_path: str, text: str, output_path: str):
    print(f"🧠 모델로 음성 생성 중: {text}")
    # 실제 onnx를 불러와서 음성 생성하는 로직 필요
    dummy_audio = np.random.uniform(-1, 1, 22050 * 2).astype('float32')  # 2초짜리
    sf.write(output_path, dummy_audio, 22050)
    time.sleep(1)
