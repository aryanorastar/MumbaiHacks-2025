#!/bin/bash

# Arogya Sentinel - Healthcare Surge Prediction System
# Quick Launch Script for Maharashtra Hackathon Demo

echo "🏥 Arogya Sentinel - Healthcare Surge Prediction System"
echo "========================================================"
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first."
    echo "   Run: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Check if required packages are installed
echo "📦 Checking dependencies..."
python -c "import streamlit, plotly, pandas" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Installing missing dependencies..."
    pip install streamlit plotly pandas
fi

# Kill any existing Streamlit processes
echo "🔄 Stopping existing Streamlit processes..."
pkill -f streamlit 2>/dev/null || true

# Launch the demo
echo ""
echo "🚀 Launching Arogya Sentinel Demo..."
echo "   Opening web interface at: http://localhost:8501"
echo ""
echo "📋 Demo Instructions:"
echo "   1. Try 'Low Risk' and 'High Risk' quick tests"
echo "   2. Run full analysis with different cities"
echo "   3. Explore all tabs in the results"
echo ""
echo "⏹️  Press Ctrl+C to stop the demo"
echo ""

# Launch Streamlit demo
streamlit run demo_app.py --server.port 8501 --server.headless false --browser.gatherUsageStats false

echo ""
echo "✅ Demo stopped. Thank you for using Arogya Sentinel!"
