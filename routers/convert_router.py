from fastapi import APIRouter
from utils.model_converter import convert_to_onnx

router = APIRouter()

@router.post("/convert_model/")
def convert_user_model(user_id: str):
    convert_to_onnx(user_id)
    return {"message": "모델 변환 완료"}
