@echo off
REM CCTV Analyzer - Windows Setup Script

echo ========================================
echo 🎥 CCTV Analyzer - Setup Script
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ℹ️  Virtual environment already exists
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo ✅ Dependencies installed successfully
) else (
    echo ❌ Error installing dependencies
    pause
    exit /b 1
)

echo.
echo ========================================
echo 🎉 Setup Complete!
echo ========================================
echo.
echo 📝 Next Steps:
echo.
echo 1. Get your Google AI Studio API key:
echo    👉 https://aistudio.google.com/
echo.
echo 2. Prepare a sample CCTV video (MP4, AVI, MOV, or MKV)
echo.
echo 3. Run the application:
echo    streamlit run app.py
echo.
echo 4. Open your browser at http://localhost:8501
echo.
echo ========================================
echo.

REM Ask if user wants to launch now
set /p launch="Would you like to launch the app now? (Y/N): "
if /i "%launch%"=="Y" (
    echo.
    echo 🚀 Launching CCTV Analyzer...
    streamlit run app.py
)

pause
