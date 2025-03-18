from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class TrainRequest(BaseModel):
    user_id: str

@router.post("/train_model/")
def train_user_model(request: TrainRequest):
    user_id = request.user_id
    model_output_path = f"backup/{user_id}/{user_id}_voice_model.onnx"

    # 🔹 음성 파일 경로 확인
    user_audio_path = f"backup/{user_id}/my_voice_complete.m4a"
    if not os.path.exists(user_audio_path):
        raise HTTPException(status_code=404, detail="음성 파일이 존재하지 않습니다.")

    # 🔹 ONNX 학습 모델 생성 (가짜 학습 코드)
    with open(model_output_path, "w") as f:
        f.write("ONNX Model Data")  # ✅ 실제 학습 코드 대체 가능

    return {"message": "모델 학습 완료", "model_path": model_output_path}
