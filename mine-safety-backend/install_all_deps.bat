@echo off
echo Installing all required dependencies...
echo.

pip install ultralytics
pip install opencv-python
pip install onnx
pip install numpy
pip install pillow

echo.
echo ✓ All dependencies installed!
echo.
echo Now restart your FastAPI server:
echo python -m uvicorn main:app --reload
echo.
pause
