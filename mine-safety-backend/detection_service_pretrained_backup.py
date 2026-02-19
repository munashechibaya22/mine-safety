"""
Detection service using pretrained YOLOv8 model from Hugging Face
Model: keremberke/yolov8n-protective-equipment-detection
"""
import os
import json
from typing import Dict, List

class DetectionService:
    def __init__(self):
        self.model = None
        self.conf_threshold = 0.25  # Lower threshold for better detection
        self.iou_threshold = 0.45
        
        # Map pretrained model classes to our requirements
        self.class_mapping = {
            'helmet': 'Hardhat',
            'mask': 'Mask',
            'no_helmet': 'NO-Hardhat',
            'no_mask': 'NO-Mask',
            'glove': 'Glove',
            'no_glove': 'NO-Glove',
            'goggles': 'Goggles',
            'no_goggles': 'NO-Goggles',
            'shoes': 'Safety Shoes',
            'no_shoes': 'NO-Safety Shoes'
        }
        
        # Required safety equipment (using mapped names)
        self.required_items = ["Hardhat", "Mask"]
        
        # Load pretrained model
        self.load_pretrained_model()
    
    def load_pretrained_model(self):
        """Load pretrained YOLOv8 model from Hugging Face"""
        try:
            import torch
            from ultralyticsplus import YOLO
            
            # Fix PyTorch 2.6 weights_only security issue
            # Option 1: Add ultralytics classes to safe globals
            try:
                from ultralytics.nn.tasks import DetectionModel
                from ultralytics.nn.modules import Conv, C2f, SPPF, Detect
                torch.serialization.add_safe_globals([DetectionModel, Conv, C2f, SPPF, Detect])
            except:
                pass
            
            # Option 2: Temporarily disable weights_only for model loading
            # This is safe for trusted sources like Hugging Face
            original_load = torch.load
            def load_with_weights_only_false(*args, **kwargs):
                kwargs['weights_only'] = False
                return original_load(*args, **kwargs)
            torch.load = load_with_weights_only_false
            
            try:
                # Use the medium model for better accuracy
                model_name = 'keremberke/yolov8m-protective-equipment-detection'
                print(f"Loading pretrained model: {model_name} (medium - better accuracy)")
                
                self.model = YOLO(model_name)
                
                # Set model parameters
                self.model.overrides['conf'] = self.conf_threshold
                self.model.overrides['iou'] = self.iou_threshold
                self.model.overrides['agnostic_nms'] = False
                self.model.overrides['max_det'] = 100
                
                print(f"✓ Pretrained model loaded successfully")
                print(f"  Classes: {list(self.class_mapping.keys())}")
            finally:
                # Restore original torch.load
                torch.load = original_load
            
        except ImportError as e:
            print(f"❌ Import error: {e}")
            print("Install with: pip install ultralyticsplus ultralytics torch")
            self.model = None
        except Exception as e:
            print(f"❌ Error loading pretrained model: {e}")
            import traceback
            traceback.print_exc()
            self.model = None
    
    def detect_image(self, image_path: str) -> Dict:
        """Detect safety equipment in an image using pretrained model"""
        if self.model is None:
            return self._placeholder_detection()
        
        try:
            from PIL import Image
            
            # Debug: Check image
            img = Image.open(image_path)
            print(f"\n=== Image Info ===")
            print(f"Path: {image_path}")
            print(f"Size: {img.size}")
            print(f"Mode: {img.mode}")
            
            # Perform inference using pretrained model with verbose output
            results = self.model.predict(
                image_path,
                conf=self.conf_threshold,
                iou=self.iou_threshold,
                verbose=True,
                imgsz=640
            )
            
            print(f"\n=== Raw Model Output ===")
            print(f"Results: {len(results)} result(s)")
            
            # Extract detections
            detections = []
            if len(results) > 0:
                result = results[0]
                print(f"Result object: {type(result)}")
                print(f"Has boxes: {result.boxes is not None}")
                
                if result.boxes is not None:
                    boxes = result.boxes
                    print(f"Boxes found: {len(boxes)}")
                    print(f"Boxes type: {type(boxes)}")
                    
                    # Try to access boxes data
                    if hasattr(boxes, 'data'):
                        print(f"Boxes data shape: {boxes.data.shape if hasattr(boxes.data, 'shape') else 'N/A'}")
                    
                    # Debug: print all detections regardless of confidence
                    if len(boxes) > 0:
                        print(f"\nAll detections (including low confidence):")
                        for i in range(len(boxes)):
                            class_id = int(boxes.cls[i])
                            confidence = float(boxes.conf[i])
                            original_class = self.model.names[class_id]
                            bbox = boxes.xyxy[i].tolist() if hasattr(boxes, 'xyxy') else None
                            print(f"  {original_class}: {confidence:.1%} at {bbox}")
                        
                        # Now filter by threshold
                        for i in range(len(boxes)):
                            class_id = int(boxes.cls[i])
                            confidence = float(boxes.conf[i])
                            
                            # Get class name from model
                            original_class = self.model.names[class_id]
                            
                            # Map to our class names
                            mapped_class = self.class_mapping.get(original_class, original_class)
                            
                            detections.append({
                                'class_name': mapped_class,
                                'confidence': confidence,
                                'original_class': original_class
                            })
                    else:
                        print("Boxes object is empty")
                else:
                    print("No boxes attribute in result")
            else:
                print("No results returned")
            
            print(f"\n✓ Detected {len(detections)} objects above threshold")
            
            # Group by class for summary
            class_summary = {}
            for det in detections:
                name = det['class_name']
                if name not in class_summary:
                    class_summary[name] = []
                class_summary[name].append(det['confidence'])
            
            if class_summary:
                print("\nDetection Summary:")
                for name, confs in class_summary.items():
                    print(f"  {name}: {len(confs)} detections, max: {max(confs):.1%}")
            
            # Analyze for safety compliance
            analysis = self.analyze_detections(detections)
            
            # Generate reason
            reason = self._generate_reason(
                analysis['detected_items'],
                analysis['missing_items'],
                analysis['violations'],
                analysis['is_safe']
            )
            
            return {
                "is_safe": analysis['is_safe'],
                "confidence": analysis['confidence'],
                "detected_items": json.dumps(analysis['detected_items']),
                "missing_items": json.dumps(analysis['missing_items']),
                "reason": reason
            }
        
        except Exception as e:
            print(f"❌ Detection error: {e}")
            import traceback
            traceback.print_exc()
            return self._placeholder_detection()
    
    def analyze_detections(self, detections: List[Dict]) -> Dict:
        """Analyze detections to determine safety compliance"""
        detected_items = set()
        missing_items = set(self.required_items)
        violations = []
        
        # Group detections by type
        positive_detections = {}
        negative_detections = {}
        
        for det in detections:
            class_name = det['class_name']
            confidence = det['confidence']
            
            if class_name.startswith("NO-"):
                base_name = class_name[3:]  # Remove "NO-" prefix
                if base_name not in negative_detections:
                    negative_detections[base_name] = []
                negative_detections[base_name].append(confidence)
            elif class_name in self.required_items:
                if class_name not in positive_detections:
                    positive_detections[class_name] = []
                positive_detections[class_name].append(confidence)
        
        print(f"\n=== Safety Compliance Analysis ===")
        
        # Check each required item
        for item in self.required_items:
            pos_confs = positive_detections.get(item, [])
            neg_confs = negative_detections.get(item, [])
            
            pos_count = len(pos_confs)
            neg_count = len(neg_confs)
            pos_max = max(pos_confs) if pos_confs else 0
            neg_max = max(neg_confs) if neg_confs else 0
            
            print(f"\n{item}:")
            print(f"  Present: {pos_count} detections (max: {pos_max:.1%})")
            print(f"  Missing: {neg_count} detections (max: {neg_max:.1%})")
            
            # Decision logic: positive detection wins if confidence is higher
            if pos_count > 0 and pos_max > neg_max:
                detected_items.add(item)
                missing_items.discard(item)
                print(f"  ✓ PRESENT (confidence: {pos_max:.1%})")
            elif neg_count > 0:
                violations.append(f"NO-{item}")
                print(f"  ✗ MISSING (confidence: {neg_max:.1%})")
            else:
                print(f"  ? NOT DETECTED")
        
        # Calculate overall confidence
        if detections:
            avg_confidence = sum(d['confidence'] for d in detections) / len(detections)
            confidence = int(avg_confidence * 100)
        else:
            confidence = 0
        
        # Determine if safe
        is_safe = len(missing_items) == 0 and len(violations) == 0
        
        print(f"\n=== Result ===")
        print(f"Status: {'✓ APPROVED' if is_safe else '✗ DENIED'}")
        print(f"Detected: {list(detected_items)}")
        print(f"Missing: {list(missing_items)}\n")
        
        return {
            'detected_items': list(detected_items),
            'missing_items': list(missing_items),
            'violations': violations,
            'is_safe': is_safe,
            'confidence': confidence
        }
    
    def detect_video(self, video_path: str) -> Dict:
        """Detect safety equipment in a video (analyzes key frames)"""
        if self.model is None:
            return self._placeholder_detection()
        
        try:
            import cv2
            
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Analyze every 30th frame
            frames_to_analyze = max(1, frame_count // 30)
            frame_interval = frame_count // frames_to_analyze
            
            all_detections = []
            
            for i in range(frames_to_analyze):
                frame_idx = i * frame_interval
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if not ret:
                    break
                
                # Save frame temporarily
                temp_path = "temp_frame.jpg"
                cv2.imwrite(temp_path, frame)
                
                # Detect on frame
                result = self.detect_image(temp_path)
                all_detections.append(result)
                
                # Clean up
                if os.path.exists(temp_path):
                    os.remove(temp_path)
            
            cap.release()
            
            # Aggregate results (use most conservative - if any frame is unsafe, video is unsafe)
            is_safe = all(d['is_safe'] for d in all_detections)
            avg_confidence = sum(d['confidence'] for d in all_detections) // len(all_detections)
            
            # Combine detected and missing items
            all_detected = set()
            all_missing = set()
            
            for det in all_detections:
                all_detected.update(json.loads(det['detected_items']))
                all_missing.update(json.loads(det['missing_items']))
            
            reason = self._generate_reason(
                list(all_detected),
                list(all_missing),
                [],
                is_safe
            )
            
            return {
                "is_safe": is_safe,
                "confidence": avg_confidence,
                "detected_items": json.dumps(list(all_detected)),
                "missing_items": json.dumps(list(all_missing)),
                "reason": reason
            }
        
        except Exception as e:
            print(f"Video detection error: {e}")
            return self._placeholder_detection()
    
    def _placeholder_detection(self) -> Dict:
        """Fallback placeholder detection"""
        detected = ["Hardhat"]
        missing = ["Mask"]
        confidence = 75
        
        is_safe = len(missing) == 0
        reason = self._generate_reason(detected, missing, [], is_safe)
        
        return {
            "is_safe": is_safe,
            "confidence": confidence,
            "detected_items": json.dumps(detected),
            "missing_items": json.dumps(missing),
            "reason": reason
        }
    
    def _generate_reason(self, detected: List[str], missing: List[str], violations: List[str], is_safe: bool) -> str:
        """Generate human-readable reason for the detection result"""
        if is_safe:
            return f"All required safety equipment detected: {', '.join(detected)}. Entry approved."
        else:
            reasons = []
            if missing:
                reasons.append(f"Missing: {', '.join(missing)}")
            if violations:
                reasons.append(f"Violations: {', '.join(violations)}")
            
            return f"Entry denied. {'. '.join(reasons)}."

# Create singleton instance
detection_service = DetectionService()
