# from fastapi import APIRouter, UploadFile, File, Form
# from pydantic import BaseModel
# from typing import List
# import os
# import json
# from utils.tts_engine import synthesize_with_model  # 음성합성 함수

# # ✅ FastAPI 라우터 객체 생성
# router = APIRouter()

# # ✅ 파일명 지정 딕셔너리
# AUDIO_FILENAME = {
#     "father": "audio_father_AI.m4a",
#     "mother": "audio_mother_AI.m4a"
# }

# # ✅ 요청 데이터 모델
# class TTSRequest(BaseModel):
#     folderName: str
#     text: str

# # ✅ 음성합성 라우터
# @router.post("/synthesize_batch/")
# async def synthesize_batch(
#     user_id: str = Form(...),
#     voice_type: str = Form(...),
#     requests: str = Form(...),
#     model_url: str = Form(...)  # ✅ URL로 ONNX 모델 전달
# ):
#     try:
#         req_list: List[TTSRequest] = [TTSRequest(**r) for r in json.loads(requests)]
#     except Exception as e:
#         return {"error": f"JSON 파싱 오류: {str(e)}"}

#     # 모델 다운로드 후 임시 저장
#     model_dir = f"./tmp_models/{user_id}"
#     os.makedirs(model_dir, exist_ok=True)
#     model_path = os.path.join(model_dir, "model.onnx")

#     try:
#         res = requests.get(model_url)
#         with open(model_path, "wb") as f:
#             f.write(res.content)
#         print(f"✅ 모델 다운로드 성공: {model_path}")
#     except Exception as e:
#         return {"error": f"모델 다운로드 실패: {str(e)}"}

#     result_folders = []

#     # 페이지별로 음성 생성
#     for item in req_list:
#         folder_path = os.path.join("backup", user_id, item.folderName)
#         os.makedirs(folder_path, exist_ok=True)

#         save_path = os.path.join(folder_path, AUDIO_FILENAME[voice_type])
#         synthesize_with_model(text=item.text, model_path=model_path, output_path=save_path)

#         result_folders.append(item.folderName)

#     # 모델 파일 삭제
#     os.remove(model_path)

#     return {"filenames": result_folders}



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
