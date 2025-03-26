
# routes/synthesize.py
from fastapi import APIRouter, UploadFile, File, Form
from typing import List
from utils.synthesizer import synthesize_speech
import shutil
import os
import uuid
from fastapi.responses import FileResponse

router = APIRouter()

@router.post("/synthesize/")
async def synthesize(
    model: UploadFile = File(...),
    texts: List[str] = Form(...)
):
    # 1️⃣ 임시 저장 경로 생성
    session_id = str(uuid.uuid4())
    work_dir = f"temp/{session_id}"
    os.makedirs(work_dir, exist_ok=True)
    
    model_path = os.path.join(work_dir, model.filename)

    # 2️⃣ 모델 저장
    with open(model_path, "wb") as buffer:
        shutil.copyfileobj(model.file, buffer)

    output_files = []
    for idx, text in enumerate(texts):
        output_path = os.path.join(work_dir, f"speech_{idx+1}.wav")
        synthesize_speech(model_path, text, output_path)
        output_files.append(output_path)

    # 3️⃣ zip으로 묶기
    import zipfile
    zip_path = os.path.join(work_dir, "output_audio.zip")
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for file in output_files:
            zipf.write(file, arcname=os.path.basename(file))

    return FileResponse(zip_path, filename="synthesized_audio.zip", media_type='application/zip')
