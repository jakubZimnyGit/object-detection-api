from ultralytics import YOLO

def load_model(model_path="yolov8n.pt"):
    model = YOLO(model_path)
    return model