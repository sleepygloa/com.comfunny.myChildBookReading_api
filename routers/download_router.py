from fastapi.responses import FileResponse
import os
from config import MODEL_DIR

router = APIRouter()

@router.get("/download_model/")
async def download_model(user_id: str):
    model_path = os.path.join(MODEL_DIR, f"{user_id}_voice_model.onnx")
    
    if os.path.exists(model_path):
        return FileResponse(model_path, media_type='application/octet-stream', filename=f"{user_id}_voice_model.onnx")
    return {"error": "파일이 존재하지 않습니다."}
