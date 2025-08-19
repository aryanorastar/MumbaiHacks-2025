@echo off
REM Arogya Sentinel - Healthcare Surge Prediction System
REM Quick Launch Script for Maharashtra Hackathon Demo (Windows)

echo 🏥 Arogya Sentinel - Healthcare Surge Prediction System
echo ========================================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo ❌ Virtual environment not found. Please run setup first.
    echo    Run: python -m venv venv ^&^& venv\Scripts\activate ^&^& pip install -r requirements.txt
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate

REM Check if required packages are installed
echo 📦 Checking dependencies...
python -c "import streamlit, plotly, pandas" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Installing missing dependencies...
    pip install streamlit plotly pandas
)

REM Kill any existing Streamlit processes
echo 🔄 Stopping existing Streamlit processes...
taskkill /f /im streamlit.exe >nul 2>&1

REM Launch the demo
echo.
echo 🚀 Launching Arogya Sentinel Demo...
echo    Opening web interface at: http://localhost:8501
echo.
echo 📋 Demo Instructions:
echo    1. Try 'Low Risk' and 'High Risk' quick tests
echo    2. Run full analysis with different cities
echo    3. Explore all tabs in the results
echo.
echo ⏹️ Press Ctrl+C to stop the demo
echo.

REM Launch Streamlit demo
streamlit run demo_app.py --server.port 8501 --server.headless false --browser.gatherUsageStats false

echo.
echo ✅ Demo stopped. Thank you for using Arogya Sentinel!
pause
