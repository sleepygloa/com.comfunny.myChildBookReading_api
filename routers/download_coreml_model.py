from fastapi.responses import FileResponse
from fastapi import APIRouter, HTTPException
import os
import coremltools as ct
import onnx

router = APIRouter()
MODEL_DIR = "backup"

def convert_onnx_to_coreml(user_id: str):
    """ 🔄 ONNX 모델을 CoreML로 변환 """
    onnx_model_path = os.path.join(MODEL_DIR, f"{user_id}/{user_id}_voice_model.onnx")
    coreml_model_path = os.path.join(MODEL_DIR, f"{user_id}/{user_id}_voice_model.mlmodel")

    if not os.path.exists(onnx_model_path):
        raise FileNotFoundError("ONNX 모델이 존재하지 않습니다.")

    # ONNX 모델 로드
    onnx_model = onnx.load(onnx_model_path)

    # ONNX → CoreML 변환
    coreml_model = ct.converters.onnx.convert(model=onnx_model)

    # 변환된 CoreML 모델 저장
    coreml_model.save(coreml_model_path)
    return coreml_model_path

@router.get("/download_coreml/")
async def download_coreml_model(user_id: str):
    """ 📥 CoreML 모델 다운로드 """
    try:
        coreml_model_path = convert_onnx_to_coreml(user_id)
        
        if os.path.exists(coreml_model_path):
            return FileResponse(coreml_model_path, media_type='application/octet-stream', filename=f"{user_id}_voice_model.mlmodel")
        else:
            raise HTTPException(status_code=404, detail="CoreML 모델이 존재하지 않습니다.")
    
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
