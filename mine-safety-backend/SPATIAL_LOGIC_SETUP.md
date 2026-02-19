# Spatial Logic Detection Setup

## What Changed?

Switched from simple confidence-based detection to **spatial logic** that:

1. Detects all objects in the image (people + equipment)
2. Finds the primary person (largest bounding box = closest to camera)
3. Matches equipment to that person using spatial overlap (30% threshold)
4. Only approves if required equipment is ON the person

## Why This Works Better

Your previous model had issues because it tried to detect "NO-Hardhat" and "NO-Mask" as separate classes, which confused the model. The spatial approach:

- Only detects positive items (Hardhat, Safety Vest, Person)
- Uses geometry to determine if equipment belongs to the person
- More reliable and logical

## Model Location

The service will try to load models in this order:

1. `miner_safety/yolo11s_production/weights/best.onnx` (your new Gemini model)
2. `best.onnx` (your old model as fallback)

## Required Classes

Your model must detect these classes:
- `Person` - The worker
- `Hardhat` - Hard hat/helmet
- `Safety Vest` - High-visibility vest

Optional classes (will be detected but not required):
- `Mask`, `Gloves`, `Safety Shoes`, etc.

## How It Works

```
1. Image → YOLO Model
   ↓
2. Separate detections:
   - Persons: [(x1,y1,x2,y2), ...]
   - Gear: [{"name": "Hardhat", "coords": (x1,y1,x2,y2)}, ...]
   ↓
3. Find largest person (closest to camera)
   ↓
4. For each gear item:
   - Calculate overlap with person bounding box
   - If overlap > 30% → gear belongs to person
   ↓
5. Check if person has all required gear
   - Has Hardhat? ✓
   - Has Safety Vest? ✓
   ↓
6. Result: APPROVED or DENIED
```

## Testing

Restart your FastAPI server and test with an image:

```bash
python -m uvicorn main:app --reload
```

Then upload an image through the web interface.

## Expected Output

```
=== Spatial Detection Analysis ===
Image: uploads/test.jpg
Size: (1280, 720)
  Person detected: conf=92.3%
  Hardhat detected: conf=87.5%
  Safety Vest detected: conf=89.2%

Primary person identified (largest bounding box)

Matching gear to person (overlap threshold: 30%):
  ✓ Hardhat: 65.3% overlap - MATCHED
  ✓ Safety Vest: 72.1% overlap - MATCHED

=== Result ===
Status: ✓ APPROVED
Detected on person: ['Hardhat', 'Safety Vest']
Missing: []
```

## Troubleshooting

### No person detected
- Make sure your model has a "Person" class
- Check if confidence threshold (0.45) is too high
- Try lowering to 0.35 in `detection_service.py`

### Equipment not matching to person
- The overlap threshold is 30%
- If equipment is far from person, it won't match
- This is intentional - we only want equipment ON the person

### Model not loading
- Check that model file exists at the specified path
- Make sure `ultralytics` is installed: `pip install ultralytics`
- Check console output for error messages

## Configuration

Edit `detection_service.py` to adjust:

```python
# Confidence threshold for detections
self.conf_threshold = 0.45  # Lower = more detections

# Required equipment
self.required_items = ["Hardhat", "Safety Vest"]  # Add/remove items

# Overlap threshold for matching gear to person
overlap_threshold = 0.30  # 30% overlap required
```

## For Your School Project

This approach is much more professional and shows you understand:
- Computer vision fundamentals
- Spatial reasoning
- Real-world problem solving

You can explain in your presentation:
- "We use spatial logic to match equipment to specific workers"
- "This prevents false positives from equipment in the background"
- "The system finds the person closest to the camera (largest box) and verifies their equipment"

Much better than just "the model detects things"!
