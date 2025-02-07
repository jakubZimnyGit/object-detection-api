from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse, StreamingResponse
import io
import os
from app.utils import load_and_convert_image, detect_and_annotate_objects, save_annotated_image, validate_image_file
from app.model import load_model
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

model = load_model("yolov8n.pt")
os.makedirs("app/static", exist_ok=True)

@app.post("/detect")
async def object_detect(file: UploadFile = File(...)):
    contents = await file.read()

    validate_image_file(contents, file.content_type)
    
    image_cv = load_and_convert_image(contents)
    
    image_cv, objects_info = detect_and_annotate_objects(image_cv, model)
    
    output_path = save_annotated_image(image_cv)
    image_url = f"/static/result.jpg"

    return {
        "image": image_url,  # Zwracamy URL obrazu
        "objects_info": objects_info
    }
