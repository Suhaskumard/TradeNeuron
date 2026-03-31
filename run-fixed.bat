@echo off
echo Starting TradeNeuron - Fixed version
cd /d "f:/Projects/TradeNeuron"

REM Use pipx for deps
pipx install uvicorn
pipx install fastapi
pipx inject uvicorn "uvicorn[standard]"

REM Or force global install
pip install --break-system-packages -r requirements.txt --force-reinstall

echo API starting...
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload

echo Dashboard: streamlit run dashboard/app.py
echo Visit: http://localhost:8001 ^|^| http://localhost:8501
pause

