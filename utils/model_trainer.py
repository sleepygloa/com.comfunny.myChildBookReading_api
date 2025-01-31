import torch
import os
from config import UPLOAD_DIR, MODEL_DIR

def train_model(user_id: str):
    user_dir = os.path.join(UPLOAD_DIR, user_id)
    if not os.path.exists(user_dir):
        raise FileNotFoundError("사용자의 음성 데이터가 없습니다.")

    # 📌 간단한 PyTorch 모델 예제
    model = torch.nn.Linear(10, 1)  
    torch.save(model.state_dict(), os.path.join(MODEL_DIR, f"{user_id}_voice_model.pth"))
    print(f"✅ {user_id}의 모델 학습 완료")
