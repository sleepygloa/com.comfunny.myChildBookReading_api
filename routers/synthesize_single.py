from fastapi import APIRouter, Form
from pydantic import BaseModel
from typing import List
import os, json, requests, zipfile
from fastapi.responses import FileResponse
from utils.tts_engine import synthesize_to_memory
from io import BytesIO
import tempfile
import uuid

router = APIRouter()

class TTSRequest(BaseModel):
    folderName: str
    text: str

AUDIO_FILENAME = {
    "father": "audio_father_AI.m4a",
    "mother": "audio_mother_AI.m4a"
}

@router.post("/synthesize_single/")
async def synthesize_single(
    user_id: str = Form(...),
    voice_type: str = Form(...),
    folder_name: str = Form(...),
    text: str = Form(...),
    model_url: str = Form(...)
):
    try:
        req_list: List[TTSRequest] = [TTSRequest(**r) for r in json.loads(requests)]
    except Exception as e:
        return {"error": f"JSON 파싱 오류: {str(e)}"}

    # 모델 다운로드
    tmp_model_path = f"/tmp/model_{uuid.uuid4().hex}.onnx"
    try:
        res = requests.get(model_url)
        with open(tmp_model_path, "wb") as f:
            f.write(res.content)
    except Exception as e:
        return {"error": f"모델 다운로드 실패: {str(e)}"}


    audio_bytes = synthesize_to_memory(text=text, model_path=tmp_model_path)

    # 폴더명을 파일명으로 사용, 예: page1/audio_mother_AI.m4a
    filename = f"{folderName}/{AUDIO_FILENAME[voice_type]}"
    # synthesize_to_memory → m4a 바이너리 생성 후 리턴
    audio_bytes = synthesize_to_memory(text=text, model_path=model_path)
    return Response(content=audio_bytes, media_type='audio/m4a')
    # zipf.writestr(filename, audio_bytes)
