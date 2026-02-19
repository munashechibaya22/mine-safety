from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
import uvicorn
from datetime import timedelta
import os
import shutil
from pathlib import Path

from database import engine, get_db, Base
import models
import schemas
from auth import (
    get_password_hash,
    verify_password,
    create_access_token,
    get_current_user
)
from config import settings
from detection_service import detection_service

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mine Safety Detection API")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Mount uploads directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.get("/")
def read_root():
    return {"message": "Mine Safety Detection API", "status": "running"}

# Auth endpoints
@app.post("/api/auth/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/api/auth/login", response_model=schemas.Token)
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/auth/me", response_model=schemas.User)
def get_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# Detection endpoints
@app.post("/api/detect", response_model=schemas.DetectionResponse)
async def detect_safety(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Validate file type
    allowed_types = ["image/jpeg", "image/png", "image/jpg", "video/mp4", "video/avi"]
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    # Save uploaded file
    if file.filename:
        file_extension = file.filename.split(".")[-1]
    else:
        file_extension = "jpg"  # Default extension
    
    file_path = UPLOAD_DIR / f"{current_user.id}_{file.filename or 'upload.jpg'}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Determine file type and run detection
    file_type = "image" if file.content_type.startswith("image") else "video"
    
    if file_type == "image":
        result = detection_service.detect_image(str(file_path))
    else:
        result = detection_service.detect_video(str(file_path))
    
    # Save detection to database
    detection = models.Detection(
        user_id=current_user.id,
        file_path=str(file_path),
        file_type=file_type,
        is_safe=result["is_safe"],
        confidence=result["confidence"],
        detected_items=result["detected_items"],
        missing_items=result["missing_items"],
        reason=result["reason"]
    )
    db.add(detection)
    db.commit()
    db.refresh(detection)
    
    return detection

@app.get("/api/detections", response_model=list[schemas.DetectionResponse])
def get_detections(
    skip: int = 0,
    limit: int = 50,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    detections = db.query(models.Detection).filter(
        models.Detection.user_id == current_user.id
    ).order_by(models.Detection.created_at.desc()).offset(skip).limit(limit).all()
    return detections

@app.get("/api/dashboard", response_model=schemas.DashboardStats)
def get_dashboard_stats(
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    total_detections = db.query(models.Detection).filter(
        models.Detection.user_id == current_user.id
    ).count()
    
    total_accepted = db.query(models.Detection).filter(
        models.Detection.user_id == current_user.id,
        models.Detection.is_safe == True
    ).count()
    
    total_denied = db.query(models.Detection).filter(
        models.Detection.user_id == current_user.id,
        models.Detection.is_safe == False
    ).count()
    
    recent_detections = db.query(models.Detection).filter(
        models.Detection.user_id == current_user.id
    ).order_by(models.Detection.created_at.desc()).limit(10).all()
    
    return {
        "total_detections": total_detections,
        "total_accepted": total_accepted,
        "total_denied": total_denied,
        "recent_detections": recent_detections
    }

if __name__ == "__main__":
    
    uvicorn.run(app, host="0.0.0.0", port=8000)
