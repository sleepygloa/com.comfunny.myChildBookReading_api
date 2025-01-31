import torch
import os
from config import MODEL_DIR

def convert_to_onnx(user_id: str):
    model_path = os.path.join(MODEL_DIR, f"{user_id}_voice_model.pth")
    onnx_path = os.path.join(MODEL_DIR, f"{user_id}_voice_model.onnx")

    if not os.path.exists(model_path):
        raise FileNotFoundError("학습된 모델이 없습니다.")

    model = torch.nn.Linear(10, 1)  
    model.load_state_dict(torch.load(model_path))

    dummy_input = torch.randn(1, 10)
    torch.onnx.export(model, dummy_input, onnx_path)

    print(f"✅ {user_id}의 모델 ONNX 변환 완료")
