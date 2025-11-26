import os
from fastapi.testclient import TestClient
from app.main import app
import io

client = TestClient(app)

def test_root():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_upload_and_stats_and_ml(tmp_path):
    # create a small csv
    csv = "a,b,target\n1,2,0\n2,3,1\n3,4,0\n4,5,1\n"
    files = {"file": ("test.csv", io.BytesIO(csv.encode()), "text/csv")}
    r = client.post("/upload", files=files)
    assert r.status_code == 200
    file_id = r.json()["file_id"]

    # stats
    r2 = client.post(f"/stats/{file_id}")
    assert r2.status_code == 200
    assert "stats" in r2.json()

    # train ML (target column "target")
    r3 = client.post(f"/ml/train/{file_id}", params={"target":"target"})
    assert r3.status_code == 200
    assert "ml_report" in r3.json()
