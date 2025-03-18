from fastapi import APIRouter, HTTPException
import os
import librosa
import numpy as np
import torch

router = APIRouter()

UPLOAD_DIR = "backup"
MODEL_DIR = "models"

def train_voice_model(audio_path, output_model_path):
    """ 🎤 음성 파일을 학습하여 ONNX 모델 변환 """
    y, sr = librosa.load(audio_path, sr=16000)
    features = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)

    class SimpleVoiceModel(torch.nn.Module):
        def __init__(self):
            super(SimpleVoiceModel, self).__init__()
            self.fc1 = torch.nn.Linear(40, 32)
            self.fc2 = torch.nn.Linear(32, 16)
            self.fc3 = torch.nn.Linear(16, 1)
        
        def forward(self, x):
            x = torch.relu(self.fc1(x))
            x = torch.relu(self.fc2(x))
            x = self.fc3(x)
            return x

    model = SimpleVoiceModel()
    dummy_input = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
    torch.onnx.export(model, dummy_input, output_model_path)

    return output_model_path

@router.post("/train_model/")
def train_user_model(user_id: str):
    """ 🏋️‍♂️ userId에 해당하는 음성 파일을 찾아 학습 """
    user_audio_path = os.path.join(UPLOAD_DIR, user_id, "my_voice_complete.m4a")
    model_output_path = os.path.join(MODEL_DIR, f"{user_id}_voice_model.onnx")

    if not os.path.exists(user_audio_path):
        raise HTTPException(status_code=404, detail="음성 파일이 존재하지 않습니다.")

    os.makedirs(MODEL_DIR, exist_ok=True)  # 🔥 모델 저장 폴더 자동 생성
    train_voice_model(user_audio_path, model_output_path)

    return {"message": "모델 학습 완료", "model_path": model_output_path}
