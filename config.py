import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 📂 저장 경로 설정
UPLOAD_DIR = os.path.join(BASE_DIR, "uploads")
MODEL_DIR = os.path.join(BASE_DIR, "models")

# 📌 폴더 생성
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)
