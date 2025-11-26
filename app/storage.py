import os
import shutil

os.makedirs("uploads", exist_ok=True)
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

def save_upload_file(upload_file, file_id):
    """Save a FastAPI UploadFile to uploads/ and copy to data/ (persisted)."""
    upload_path = f"uploads/{file_id}.csv"
    data_path = f"data/{file_id}.csv"

    with open(upload_path, "wb") as buffer:
        shutil.copyfileobj(upload_file.file, buffer)

    # Also copy to data/ for persistence
    shutil.copy(upload_path, data_path)
    return upload_path, data_path
