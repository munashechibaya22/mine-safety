"""Quick test script for detection service"""
import sys
from detection_service import detection_service

if len(sys.argv) < 2:
    print("Usage: python test_detection.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]
print(f"Testing detection on: {image_path}\n")

result = detection_service.detect_image(image_path)

print("\n" + "="*50)
print("FINAL RESULT:")
print("="*50)
print(f"Safe: {result['is_safe']}")
print(f"Confidence: {result['confidence']}%")
print(f"Reason: {result['reason']}")
print(f"Detected: {result['detected_items']}")
print(f"Missing: {result['missing_items']}")
