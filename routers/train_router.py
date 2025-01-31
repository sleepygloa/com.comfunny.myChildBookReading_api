from fastapi import APIRouter
from utils.model_trainer import train_model

router = APIRouter()

@router.post("/train_model/")
def train_user_model(user_id: str):
    train_model(user_id)
    return {"message": "모델 학습 완료"}
