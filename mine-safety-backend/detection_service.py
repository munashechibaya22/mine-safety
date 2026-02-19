import os
import json
import io
import cv2
import numpy as np
from typing import Dict, List
from PIL import Image
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel


class DetectionService:
    def __init__(self):
        self.model = None
        self.conf_threshold = 0.45
        
        # Required safety equipment
        self.required_items = ["Hardhat", "Safety Vest"]
        
        # Exact class mapping from your specific data.yaml (25 classes)
        self.class_mapping = {
            0: "Excavator",
            1: "Gloves",
            2: "Hardhat",
            3: "Ladder",
            4: "Mask",
            5: "NO-Hardhat",
            6: "NO-Mask",
            7: "NO-Safety Vest",
            8: "Person",
            9: "SUV",
            10: "Safety Cone",
            11: "Safety Vest",
            12: "bus",
            13: "dump truck",
            14: "fire hydrant",
            15: "machinery",
            16: "mini-van",
            17: "sedan",
            18: "semi",
            19: "trailer",
            20: "truck and trailer",
            21: "truck",
            22: "van",
            23: "vehicle",
            24: "wheel loader"
        }
        
        # Load model
        self.load_model()
    
    def load_model(self):
        """Load YOLO model"""
        try:
            from ultralytics import YOLO
            
            # Try to load model (check multiple possible locations)
            model_paths = [
                os.path.join(os.path.dirname(__file__), "best.onnx"),  # Same dir as this file
                "best.onnx",  # Current directory
                os.path.join(os.path.dirname(__file__), "yolov8n.pt"),  # PyTorch model fallback
                "yolov8n.pt"
            ]
            
            for model_path in model_paths:
                if not os.path.exists(model_path):
                    continue
                    
                full_path = os.path.abspath(model_path)
                print(f"Attempting to load: {full_path}")
                
                try:
                    # Explicitly declare task="detect" to suppress the Ultralytics warning
                    if model_path.endswith('.onnx'):
                        print("  Loading ONNX model...")
                        self.model = YOLO(model_path, task="detect")
                    else:
                        print("  Loading PyTorch model...")
                        self.model = YOLO(model_path, task="detect")
                    
                    if self.model is not None:
                        print(f"✓ Model loaded successfully!")
                        return
                        
                except Exception as load_error:
                    print(f"  Failed: {load_error}")
                    self.model = None
                    continue
            
            print("❌ No valid model could be loaded")
            self.model = None
            
        except ImportError as e:
            print(f"❌ ultralytics not installed: {e}")
            self.model = None
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            self.model = None
    
    def calculate_iou(self, boxA: List[float], boxB: List[float]) -> float:
        """Calculate how much Box A overlaps with Box B"""
        xA = max(boxA[0], boxB[0])
        yA = max(boxA[1], boxB[1])
        xB = min(boxA[2], boxB[2])
        yB = min(boxA[3], boxB[3])
        
        interArea = max(0, xB - xA) * max(0, yB - yA)
        if interArea == 0:
            return 0.0
        
        boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
        if boxAArea == 0:
            return 0.0
            
        return interArea / float(boxAArea)


    def detect_image(self, image: Image.Image) -> Dict:
        """Detect safety equipment using spatial logic focused ONLY on the nearest person."""
        if self.model is None:
            return self._placeholder_detection()
        
        try:
            results = self.model.predict(
                source=image, 
                conf=self.conf_threshold,
                verbose=False
            )
            
            persons = []
            gear = []
            
            for r in results:
                if r.boxes is None or len(r.boxes) == 0:
                    continue
                
                for box in r.boxes:
                    class_id = int(box.cls[0])
                    
                    # USE OUR LOCAL DICTIONARY INSTEAD OF THE MODEL'S
                    class_name = self.class_mapping.get(class_id, f"Unknown_{class_id}")
                    
                    coords = box.xyxy[0].tolist()
                    confidence = float(box.conf[0])
                    
                    if class_name == "Person":
                        persons.append({
                            'coords': coords,
                            'confidence': confidence
                        })
                    else:
                        gear.append({
                            'name': class_name,
                            'coords': coords,
                            'confidence': confidence
                        })
            
            # 1. Check if any person is in frame
            if not persons:
                return {
                    "is_safe": False,
                    "confidence": 0,
                    "detected_items": json.dumps([]),
                    "missing_items": json.dumps(self.required_items),
                    "reason": "No person detected in the frame."
                }
            
            # 2. ISOLATE NEAREST PERSON: Find the person with the largest bounding box area
            nearest_person = max(
                persons,
                key=lambda p: (p['coords'][2] - p['coords'][0]) * (p['coords'][3] - p['coords'][1])
            )
            
            # 3. ONLY match gear that physically overlaps with this specific nearest person
            nearest_person_gear = []
            overlap_threshold = 0.30
            
            for item in gear:
                overlap = self.calculate_iou(item['coords'], nearest_person['coords'])
                if overlap > overlap_threshold:
                    nearest_person_gear.append(item)
            
            # 4. Extract just the names of the gear found on the nearest person
            # Use a set to remove duplicates (e.g., if two hardhats overlap the same person)
            detected_gear_names = list(set([item['name'] for item in nearest_person_gear]))
            
            # 5. Check what is missing
            missing_items = [req for req in self.required_items if req not in detected_gear_names]
            is_safe = len(missing_items) == 0
            
            # 6. Calculate confidence ONLY from the gear on the nearest person
            if nearest_person_gear:
                avg_conf = sum(item['confidence'] for item in nearest_person_gear) / len(nearest_person_gear)
                confidence = int(avg_conf * 100)
                # Cap at 100 to be perfectly safe
                confidence = min(100, max(0, confidence))
            else:
                # If they have no gear, use the confidence of the person detection itself
                confidence = int(nearest_person['confidence'] * 100)
            
            # 7. Format the response
            reason = (f"Nearest person verified safe: {', '.join(detected_gear_names)}. Entry approved." 
                      if is_safe else 
                      f"Nearest person missing gear: {', '.join(missing_items)}.")
            
            return {
                "is_safe": is_safe,
                "confidence": confidence,
                "detected_items": json.dumps(detected_gear_names),
                "missing_items": json.dumps(missing_items),
                "reason": reason
            }
            
        except Exception as e:
            print(f"❌ Detection error: {e}")
            import traceback
            traceback.print_exc()
            return self._placeholder_detection()

            
    def detect_video(self, video_path: str) -> Dict:
        """Video detection - analyze key frames"""
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Analyze every 30th frame
            frames_to_analyze = max(1, min(frame_count // 30, 10))
            frame_interval = frame_count // frames_to_analyze if frames_to_analyze > 0 else 1
            
            all_results = []
            
            for i in range(frames_to_analyze):
                frame_idx = i * frame_interval
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Convert OpenCV BGR frame to PIL RGB Image
                color_converted = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                pil_image = Image.fromarray(color_converted)
                
                # Detect on frame
                result = self.detect_image(pil_image)
                all_results.append(result)
                
            cap.release()
            
            if not all_results:
                return self._placeholder_detection()
            
            # Use most conservative result (if any frame is unsafe, video is unsafe)
            is_safe = all(r['is_safe'] for r in all_results)
            avg_confidence = sum(r['confidence'] for r in all_results) // len(all_results)
            
            # Combine detected and missing items
            all_detected = set()
            all_missing = set()
            
            for r in all_results:
                all_detected.update(json.loads(r['detected_items']))
                all_missing.update(json.loads(r['missing_items']))
            
            if is_safe:
                reason = f"All required safety equipment verified across video frames. Entry approved."
            else:
                reason = f"Missing required safety equipment in video: {', '.join(all_missing)}."
            
            return {
                "is_safe": is_safe,
                "confidence": avg_confidence,
                "detected_items": json.dumps(list(all_detected)),
                "missing_items": json.dumps(list(all_missing)),
                "reason": reason
            }
        
        except Exception as e:
            print(f"Video detection error: {e}")
            import traceback
            traceback.print_exc()
            return self._placeholder_detection()

    def _placeholder_detection(self) -> Dict:
        """Fallback when model fails"""
        return {
            "is_safe": False,
            "confidence": 0,
            "detected_items": json.dumps([]),
            "missing_items": json.dumps(self.required_items),
            "reason": "Detection service unavailable. Please check model configuration."
        }

# Singleton instance
detection_service = DetectionService()
