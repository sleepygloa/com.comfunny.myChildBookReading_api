from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException
import os

router = APIRouter()
MODEL_DIR = "models"

@router.get("/download_model/")
async def download_model(user_id: str):
    """ 📥 학습된 모델을 다운로드 """
    model_path = os.path.join(MODEL_DIR, f"{user_id}_voice_model.onnx")

    if os.path.exists(model_path):
        return FileResponse(model_path, media_type='application/octet-stream', filename=f"{user_id}_voice_model.onnx")
    else:
        raise HTTPException(status_code=404, detail="학습된 모델이 존재하지 않습니다.")
