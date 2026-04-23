@echo off
title AI Activity Tracker - Setup
cd /d "%~dp0"

echo [1/3] Checking for Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.10 or 3.11 from python.org.
    pause
    exit /b
)

echo [2/4] Installing PyTorch with CUDA 12.1 support...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

echo [3/4] Installing fine-tuning and inference dependencies...
pip install -r requirements.txt

echo [4/4] Installing llama-cpp-python with CUDA support...
echo This requires the NVIDIA CUDA Toolkit 12.1 to be installed on your system.
pip install --prefer-binary llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cu121

echo.
echo ============================================================
echo Setup complete! 
echo.
echo If you have existing data to fine-tune, run:
echo   python scripts/convert_existing_dataset.py
echo   python scripts/finetune.py
echo   python scripts/export_gguf.py
echo.
echo Otherwise, run Activity_Tracker.bat to start tracking.
echo ============================================================
pause
