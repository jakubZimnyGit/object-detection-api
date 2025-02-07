# Object Detection API 🤖

A simple API for detecting objects in images using YOLOv8 model and FastAPI. 🖼️

### Features ✨:
- Object detection using YOLOv8 model 🔍
- FastAPI-based API for quick and efficient response times ⚡
- Frontend with React for interacting with the API 💻

### Technologies 🛠️:
- **FastAPI** 🌐
- **Python** 🐍
- **YOLOv8** (for object detection) 🧠
- **React** ⚛️
- **Uvicorn** (ASGI server) 🚀

### Installation and Setup ⚙️

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/object-detection-api.git
    cd object-detection-api
    ```

2. Set up a virtual environment:
    ```bash
    python -m venv venv
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Run the backend server 🚀:
    ```bash
    uvicorn backend.app.main:app --reload
    ```

5. (Optional) For the frontend 💻:
    - Navigate to the `frontend` folder and install the frontend dependencies:
        ```bash
        cd frontend
        npm install
        ```

    - Then run the frontend:
        ```bash
        npm run dev
        ```

Now your application should be running locally at:
- **Backend**: `http://127.0.0.1:8000`
- **Frontend**: `http://127.0.0.1:5173`

### API Endpoints 📡:

- **POST /detect**: Upload an image for object detection 🖼️➡️🔍
  - **Request**:
    - `image`: The image file you want to analyze 📸
  - **Response**:
    - Detected objects with their labels and confidence scores 🏷️✅

### Example Example 🌟:

To detect objects in an image, send a POST request to `/detect` with an image file.

#### Request:
```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/detect' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'file=@your_image.jpg'
```
#### Response:
```bash
    {
  "image": "/static/result.jpg",
  "objects_info": [
    {
      "label": "cat",
      "confidence": 0.95,
      "bounding_box": { "x1": 50, "y1": 60, "x2": 150, "y2": 200 }
    },
    {
      "label": "dog",
      "confidence": 0.89,
      "bounding_box": { "x1": 200, "y1": 250, "x2": 350, "y2": 400 }
    }
  ]
}
```

License 📝:
MIT License. See LICENSE for more details. 📄

Credits 💡:
This project uses YOLOv8 model for object detection. 🎯