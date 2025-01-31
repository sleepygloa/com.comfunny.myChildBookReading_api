import os
from config import UPLOAD_DIR

def save_uploaded_file(user_id: str, file):
    user_dir = os.path.join(UPLOAD_DIR, user_id)
    os.makedirs(user_dir, exist_ok=True)

    file_path = os.path.join(user_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())

    return file_path
