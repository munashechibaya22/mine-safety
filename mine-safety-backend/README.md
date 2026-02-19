# Mine Safety Detection Backend

FastAPI backend for mine safety equipment detection system.

## Setup

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create .env file:
```bash
cp .env.example .env
```

4. Run the server:
```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Integrating Your YOLO Model

1. Save your trained YOLO model to `models/` directory
2. Update `detection_service.py`:
   - Uncomment the YOLO import
   - Update the `load_model()` method
   - Modify detection logic in `detect_image()` and `detect_video()`

Example:
```python
from ultralytics import YOLO

def load_model(self, model_path: str):
    self.model = YOLO(model_path)

def detect_image(self, image_path: str) -> Dict:
    results = self.model(image_path)
    # Process results...
```

## Endpoints

- POST `/api/auth/register` - Register new user
- POST `/api/auth/login` - Login user
- GET `/api/auth/me` - Get current user
- POST `/api/detect` - Upload and analyze image/video
- GET `/api/detections` - Get detection history
- GET `/api/dashboard` - Get dashboard statistics
