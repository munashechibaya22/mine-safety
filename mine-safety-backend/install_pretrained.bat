@echo off
echo Installing pretrained model dependencies...
echo.

pip install ultralyticsplus==0.0.28 ultralytics==8.0.196

echo.
echo Installation complete!
echo.
echo Now restart your FastAPI server:
echo python -m uvicorn main:app --reload
echo.
pause
