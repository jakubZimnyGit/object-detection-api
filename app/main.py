from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os
from app.utils import load_and_convert_image, detect_and_annotate_objects, save_annotated_image
from app.model import load_model

app = FastAPI()

model = load_model("yolov8n.pt")
os.makedirs("static", exist_ok=True)

@app.post("/detect")
async def object_detect(file: UploadFile = File(...)):
    contents = await file.read()
    image_cv = load_and_convert_image(contents)
    
    image_cv, objects_info = detect_and_annotate_objects(image_cv, model)
    
    output_path = save_annotated_image(image_cv)

    return {
        "image": FileResponse(output_path, media_type="image/jpeg"),
        "objects_info": objects_info
    }
