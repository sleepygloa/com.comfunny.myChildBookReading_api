from fastapi import APIRouter, UploadFile, File, Form
import os

router = APIRouter()

UPLOAD_DIR = "backup"

def save_uploaded_file(user_id: str, file: UploadFile):
    """ 📂 음성 파일을 `backup/userId/` 경로에 저장 """
    user_dir = os.path.join(UPLOAD_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)  # 🔥 폴더 자동 생성

    file_path = os.path.join(user_dir, "my_voice_complete.m4a")  # 🔥 파일 저장 이름 고정
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path

@router.post("/upload_voice")
async def upload_voice(user_id: str = Form(...), file: UploadFile = File(...)):
    file_path = save_uploaded_file(user_id, file)
    return {"message": "파일 업로드 완료", "file_path": file_path}
