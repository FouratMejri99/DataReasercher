from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, JSONResponse
import uuid
from app.storage import save_upload_file
from app.analysis import compute_statistics, plot_numeric_histogram
from app.ml import train_models, predict
import os

app = FastAPI(title="Mini DTR API")

@app.get("/")
def root():
    return {"status": "ok", "message": "Mini Data-to-Research API"}

@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files allowed")
    file_id = str(uuid.uuid4())
    upload_path, data_path = save_upload_file(file, file_id)
    return {"file_id": file_id, "upload_path": upload_path, "data_path": data_path}

@app.post("/stats/{file_id}")
def stats(file_id: str):
    csv_path = f"data/{file_id}.csv"
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="file not found")
    stats, json_path = compute_statistics(csv_path)
    return {"file_id": file_id, "stats": stats, "json_path": json_path}

@app.post("/plot/{file_id}")
def plot(file_id: str, column: str):
    csv_path = f"data/{file_id}.csv"
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="file not found")
    try:
        out = plot_numeric_histogram(csv_path, column)
        return {"plot_path": out}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ml/train/{file_id}")
def ml_train(file_id: str, target: str):
    csv_path = f"data/{file_id}.csv"
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="file not found")
    try:
        result = train_models(csv_path, target)
        return JSONResponse(content={"file_id": file_id, "ml_report": result})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/ml/predict/{file_id}")
def ml_predict(file_id: str, input_row: dict, model: str = "rf"):
    csv_path = f"data/{file_id}.csv"
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="file not found")
    try:
        res = predict(csv_path, input_row, model_type=model)
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/outputs/{filename}")
def get_output(filename: str):
    path = f"outputs/{filename}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="file not found")
    # allow downloading json/png files
    return FileResponse(path)
