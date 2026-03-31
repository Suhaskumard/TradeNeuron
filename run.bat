@echo off
cd /d "f:/Projects/TradeNeuron"
echo Creating virtual environment...
python -m venv venv
echo Activating environment...
call venv\Scripts\activate.bat
echo Installing dependencies...
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
echo Starting API on http://localhost:8001
echo Open index.html in browser
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
pause

