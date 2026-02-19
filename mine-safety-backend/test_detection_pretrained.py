"""Test script for pretrained detection service"""
import sys
from detection_service_pretrained import detection_service

if len(sys.argv) < 2:
    print("Usage: python test_detection_pretrained.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]
print(f"Testing pretrained model on: {image_path}\n")
print("="*60)

result = detection_service.detect_image(image_path)

print("="*60)
print("\nFINAL RESULT:")
print("="*60)
print(f"Status: {'✓ APPROVED' if result['is_safe'] else '✗ DENIED'}")
print(f"Confidence: {result['confidence']}%")
print(f"Reason: {result['reason']}")
print(f"\nDetected Equipment: {result['detected_items']}")
print(f"Missing Equipment: {result['missing_items']}")
print("="*60)
