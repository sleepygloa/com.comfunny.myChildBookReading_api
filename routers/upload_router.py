from fastapi import APIRouter, UploadFile, File, Form
import os
from utils.file_manager import save_uploaded_file

router = APIRouter()

@router.post("/upload_voice")  # ✅ 슬래시 `/` 제거
async def upload_voice(user_id: str = Form(...), file: UploadFile = File(...)):
    file_path = save_uploaded_file(user_id, file)
    return {"message": "파일 업로드 완료", "file_path": file_path}
