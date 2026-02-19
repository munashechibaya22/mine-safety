# Model Training Issues & Solutions

## Current Problem

The YOLO model (`best.onnx`) has serious accuracy issues:

**Test Case**: Person wearing white hardhat, orange safety vest, and mask
**Expected**: Detect Hardhat, Safety Vest, Mask → APPROVED
**Actual**: Detect NO-Hardhat (70.9%), NO-Safety Vest (71.8%), Mask (69.3%) → DENIED

This is a **false negative** - the model incorrectly identifies present equipment as missing.

## Root Causes

1. **Training Data Quality**
   - Images may be mislabeled (person with hardhat labeled as "NO-Hardhat")
   - Insufficient training examples for each class
   - Imbalanced dataset (more negative examples than positive)

2. **Training Configuration**
   - Model may not have trained long enough (50 epochs might not be enough)
   - Learning rate or other hyperparameters not optimal
   - Data augmentation not sufficient

3. **Class Definition Issues**
   - Having both "Hardhat" and "NO-Hardhat" as separate classes is problematic
   - Model gets confused between presence and absence

## Recommended Solutions

### Option 1: Retrain with Better Data (RECOMMENDED)

1. **Review and clean your dataset**:
   ```bash
   # Check your training data at:
   /content/drive/MyDrive/safety/train/
   /content/drive/MyDrive/safety/valid/
   ```

2. **Verify labels are correct**:
   - Images with people wearing hardhats should be labeled "Hardhat", NOT "NO-Hardhat"
   - Check for mislabeled images

3. **Balance your dataset**:
   - Ensure roughly equal numbers of positive and negative examples
   - Add more training images if dataset is small (<500 images per class)

4. **Retrain with more epochs**:
   ```python
   model.train(
       data='/content/drive/MyDrive/safety/data.yaml',
       epochs=100,  # Increase from 50
       imgsz=640,
       patience=20,  # Early stopping
       device='0'
   )
   ```

### Option 2: Simplify Class Structure

Instead of having both "Hardhat" and "NO-Hardhat", consider:

1. **Detection-only approach**:
   - Only detect: "Hardhat", "Safety Vest", "Mask", "Person"
   - Logic: If Person detected but no Hardhat → Missing hardhat
   - Simpler and less prone to confusion

2. **Update data.yaml**:
   ```yaml
   names:
     0: Person
     1: Hardhat
     2: Safety Vest
     3: Mask
     4: Safety Cone
     5: machinery
     6: vehicle
   ```

### Option 3: Temporary Workaround (Current Implementation)

The code now includes logic to handle uncertain cases:
- If confidence difference < 5%, mark as UNCERTAIN instead of MISSING
- This reduces false negatives but doesn't fix the root cause

## Testing Your Model

After retraining, test with these scenarios:

1. **Person with all equipment** → Should APPROVE
2. **Person missing hardhat** → Should DENY (missing: Hardhat)
3. **Person missing vest** → Should DENY (missing: Safety Vest)
4. **Person missing mask** → Should DENY (missing: Mask)
5. **No person in image** → Should handle gracefully

## For Your School Project

**Short-term** (to demo now):
- Use the current model with the workaround
- Explain in your presentation that model accuracy needs improvement
- Show that the detection pipeline works correctly

**Long-term** (for better results):
- Retrain the model with cleaned, balanced data
- Consider the simplified class structure
- Train for more epochs (100-150)
- Use data augmentation (rotation, brightness, contrast)

## Model Performance Metrics

Current model shows:
- High false negative rate (detects equipment as missing when present)
- Confidence scores cluster around 50-70% (poor calibration)
- NMS working correctly (reduces from 8400 to ~4 detections)

Target metrics after retraining:
- Precision > 90% (few false positives)
- Recall > 90% (few false negatives)
- Confidence scores well-distributed (20-95% range)
