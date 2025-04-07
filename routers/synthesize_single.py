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

@router.post("/synthesize_batch/")
async def synthesize_batch(
    user_id: str = Form(...),
    voice_type: str = Form(...),
    requests: str = Form(...),
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

    # ZIP 압축 준비
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for idx, item in enumerate(req_list):
            try:
                audio_bytes = synthesize_to_memory(text=item.text, model_path=tmp_model_path)

                # 폴더명을 파일명으로 사용, 예: page1/audio_mother_AI.m4a
                filename = f"{item.folderName}/{AUDIO_FILENAME[voice_type]}"
                zipf.writestr(filename, audio_bytes)
            except Exception as e:
                print(f"❌ 변환 실패: {item.folderName} - {e}")
                continue

    # 모델 삭제
    os.remove(tmp_model_path)

    # ZIP 반환
    zip_buffer.seek(0)
    return FileResponse(
        path_or_file=zip_buffer,
        media_type="application/zip",
        filename="voices.zip"
    )
