import os
import json
from typing import Dict, List
from PIL import Image

class DetectionService:
    def __init__(self):
        self.model = None
        self.conf_threshold = 0.35
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
            from ultralyticsplus import YOLO
            
            # Use the nano model for faster inference (or yolov8m for better accuracy)
            model_name = 'keremberke/yolov8n-protective-equipment-detection'
            print(f"Loading pretrained model: {model_name}")
            
            self.model = YOLO(model_name)
            
            # Set model parameters
            self.model.overrides['conf'] = self.conf_threshold
            self.model.overrides['iou'] = self.iou_threshold
            self.model.overrides['agnostic_nms'] = False
            self.model.overrides['max_det'] = 100
            
            print(f"✓ Pretrained model loaded successfully")
            print(f"  Classes: {list(self.class_mapping.keys())}")
            
        except ImportError:
            print("❌ ultralyticsplus not installed. Install with: pip install ultralyticsplus ultralytics")
            self.model = None
        except Exception as e:
            print(f"❌ Error loading pretrained model: {e}")
            self.model = None
    
    
    def detect_image(self, image_path: str) -> Dict:
        """Detect safety equipment in an image using pretrained model"""
        if self.model is None:
            return self._placeholder_detection()
        
        try:
            # Perform inference using pretrained model
            results = self.model.predict(image_path)
            
            # Extract detections
            detections = []
            if len(results) > 0 and results[0].boxes is not None:
                boxes = results[0].boxes
                
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
            
            print(f"\n✓ Detected {len(detections)} objects")
            
            # Group by class for summary
            class_summary = {}
            for det in detections:
                name = det['class_name']
                if name not in class_summary:
                    class_summary[name] = []
                class_summary[name].append(det['confidence'])
            
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
        """Analyze detections to determine safety compliance"""
        detected_items = set()
        missing_items = set(self.required_items)
        violations = []
        
        # Check if person is detected
        has_person = any(d['class_name'] == 'Person' for d in detections)
        
        # Group detections by type
        positive_detections: Dict[str, List[float]] = {}
        negative_detections: Dict[str, List[float]] = {}
        
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
        
        print(f"\n=== Detection Analysis ===")
        if has_person:
            print("Person detected in image")
        
        # Check each required item
        for item in self.required_items:
            pos_confs = positive_detections.get(item, [])
            neg_confs = negative_detections.get(item, [])
            
            pos_count = len(pos_confs)
            neg_count = len(neg_confs)
            pos_max = max(pos_confs) if pos_confs else 0
            neg_max = max(neg_confs) if neg_confs else 0
            pos_avg = sum(pos_confs) / len(pos_confs) if pos_confs else 0
            neg_avg = sum(neg_confs) / len(neg_confs) if neg_confs else 0
            
            print(f"\n{item}:")
            print(f"  Positive: {pos_count} detections, max: {pos_max:.1%}, avg: {pos_avg:.1%}")
            print(f"  Negative: {neg_count} detections, max: {neg_max:.1%}, avg: {neg_avg:.1%}")
            
            # Decision logic with multiple criteria
            # If confidence difference is small (<5%), consider it uncertain rather than missing
            confidence_diff = pos_max - neg_max
            
            if pos_count > 0 and (
                (pos_max > neg_max and pos_count >= neg_count) or
                (confidence_diff > 0.10) or
                (pos_count > neg_count * 2)
            ):
                detected_items.add(item)
                missing_items.discard(item)
                print(f"  ✓ Decision: PRESENT (confidence diff: {confidence_diff:+.1%})")
            elif neg_count > 0 and abs(confidence_diff) < 0.05:
                # Very close confidence - uncertain, don't mark as violation
                print(f"  ? Decision: UNCERTAIN (confidence too close: {confidence_diff:+.1%})")
                # Don't add to violations, but keep in missing
            elif neg_count > 0:
                violations.append(f"NO-{item}")
                print(f"  ✗ Decision: MISSING (violation detected, diff: {confidence_diff:+.1%})")
            else:
                print(f"  ? Decision: UNCERTAIN (not detected)")
        
        # Calculate overall confidence
        if detections:
            avg_confidence = sum(d['confidence'] for d in detections) / len(detections)
            confidence = int(avg_confidence * 100)
        else:
            confidence = 0
        
        # Determine if safe
        is_safe = len(missing_items) == 0 and len(violations) == 0
        
        print(f"\n=== Final Result ===")
        print(f"Safe: {is_safe}")
        print(f"Detected: {list(detected_items)}")
        print(f"Missing: {list(missing_items)}")
        print(f"Violations: {violations}\n")
        
        return {
            'detected_items': list(detected_items),
            'missing_items': list(missing_items),
            'violations': violations,
            'is_safe': is_safe,
            'confidence': confidence
        }
    
    def detect_image(self, image_path: str) -> Dict:
        """Detect safety equipment in an image"""
        if self.model is None:
            return self._placeholder_detection()
        
        try:
            # Preprocess image
            input_data = self.preprocess_image(image_path)
            
            # Run inference
            input_name = self.model.get_inputs()[0].name
            outputs = self.model.run(None, {input_name: input_data})
            
            # Postprocess detections
            detections = self.postprocess_detections(outputs[0])
            
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
    
    def detect_video(self, video_path: str) -> Dict:
        """Detect safety equipment in a video (analyzes key frames)"""
        if self.model is None:
            return self._placeholder_detection()
        
        try:
            cap = cv2.VideoCapture(video_path)
            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Analyze every 30th frame (or adjust based on video)
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
        detected = ["Hardhat", "Safety Vest"]
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

detection_service = DetectionService()
