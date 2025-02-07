import numpy as np
import cv2
from PIL import Image
import io
from io import BytesIO
from fastapi import HTTPException

def validate_image_file(file_contents: bytes, content_type: str):
    """
    Funkcja do walidacji, czy plik jest obrazem.

    :param file_content: Zawartość pliku w formie bajtów.
    :param content_type: Typ MIME pliku.
    :raises HTTPException: Jeśli plik nie jest obrazem lub ma nieprawidłowy format.
    """
    if 'image' not in content_type:
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload an image.")
    
    try:
        Image.open(io.BytesIO(file_contents))
    except Exception:
        raise HTTPException(status_code=400, detail="Unable to identify image. Invalid file format.")
    

def load_and_convert_image(file_contents: bytes) -> np.ndarray:
    """
    Funkcja ładuje obraz z danych binarnych (np. z uploadu) i konwertuje go
    na format OpenCV.
    
    :param file_contents: Zawartość pliku obrazu w postaci bajtów.
    :return: Obraz w formacie OpenCV (np. BGR).
    """
    image = Image.open(BytesIO(file_contents))
    image_cv = np.array(image)
    image_cv = cv2.cvtColor(image_cv, cv2.COLOR_RGB2BGR)
    return image_cv


def detect_and_annotate_objects(image_cv: np.ndarray, model) -> tuple:
    """
    Funkcja wykonuje detekcję obiektów na obrazie i rysuje na nim ramki
    oraz zwraca dane o wykrytych obiektach.
    
    :param image_cv: Obraz w formacie OpenCV.
    :param model: Załadowany model detekcji obiektów (np. YOLO).
    :return: Zaktualizowany obraz oraz lista informacji o wykrytych obiektach.
    """
    results = model(image_cv)
    objects_info = []
    
    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0] if box.conf else 0.0
            label = result.names[int(box.cls[0])]
            
            cv2.rectangle(image_cv, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(image_cv, f"{label} {conf:.2f}", (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            objects_info.append({
                "label": label,
                "confidence": conf,
                "bounding_box": {
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2
                }
            })
    return image_cv, objects_info


def save_annotated_image(image_cv: np.ndarray, output_path: str = "app/static/result.jpg") -> str:
    """
    Funkcja zapisuje zmodyfikowany obraz z naniesionymi ramkami do pliku.
    
    :param image_cv: Zmieniony obraz w formacie OpenCV.
    :param output_path: Ścieżka, gdzie obraz ma zostać zapisany.
    :return: Ścieżka do zapisanego obrazu.
    """
    cv2.imwrite(output_path, image_cv)
    return output_path