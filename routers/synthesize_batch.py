# ✅ FastAPI 서버에서 클라이언트에게 JSON 리스트를 반환하는 형태로 수정
from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from typing import List
import os
import json
from utils.tts_engine import synthesize_with_model  # 사용자가 구현할 함수

app = FastAPI()

AUDIO_FILENAME = {
    "father": "audio_father_AI.m4a",
    "mother": "audio_mother_AI.m4a"
}

class TTSRequest(BaseModel):
    folderName: str
    text: str

@app.post("/synthesize_batch/")
async def synthesize_batch(
    user_id: str = Form(...),
    voice_type: str = Form(...),  # "father" or "mother"
    requests: str = Form(...),  # JSON 문자열
    model_file: UploadFile = File(...)
):
    try:
        req_list: List[TTSRequest] = [TTSRequest(**r) for r in json.loads(requests)]
    except Exception as e:
        return {"error": f"JSON 파싱 오류: {str(e)}"}

    # 모델 저장
    model_dir = f"./{user_id}"
    os.makedirs(model_dir, exist_ok=True)
    model_path = os.path.join(model_dir, model_file.filename)

    with open(model_path, "wb") as f:
        f.write(await model_file.read())

    result_folders = []

    # 각 요청에 대해 synthesize 처리
    for item in req_list:
        folder_path = os.path.join("backup", user_id, item.folderName)
        os.makedirs(folder_path, exist_ok=True)

        save_path = os.path.join(folder_path, AUDIO_FILENAME[voice_type])

        # 음성 합성 실행
        synthesize_with_model(text=item.text, model_path=model_path, output_path=save_path)

        result_folders.append(item.folderName)

    return {"filenames": result_folders}
