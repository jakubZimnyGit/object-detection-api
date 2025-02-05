import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_detect_objects():
    with open("tests/sample_image.jpg", "rb") as f:
        file_data = f.read()
    
    response = client.post("/detect", files={"file": ("sample_image.jpg", file_data, "image/jpeg")})

    assert response.status_code == 200
    assert "image" in response.json()
    assert "objects_info" in response.json()
    assert isinstance(response.json()["objects_info"], list) 

def test_invalid_file_format():
    response = client.post("/detect", files={"file": ("test.txt", b"Not an image", "text/plain")})
    assert response.status_code == 400
    assert "detail" in response.json()

def test_no_objects_in_image():
    with open("tests/empty_scene.jpg", "rb") as f:
        response = client.post("/detect", files={"file": ("empty_scene.jpg", f, "image/jpeg")})
    
    assert response.status_code == 200
    assert response.json()["objects_info"] == []

