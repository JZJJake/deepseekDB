@echo off
title AI Policy Assistant - Startup

echo ====================================================
echo Starting Policy QA Assistant (Admin and Client)
echo ====================================================
echo.

echo [1/3] Checking dependencies...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo [2/3] Checking .env file...
if not exist ".env" (
    echo Copying .env.example to .env
    copy .env.example .env >nul
)

echo [3/3] Starting Admin UI on port 8502 and Client UI on port 8501...
start "" python -m streamlit run admin_app.py --server.port 8502
timeout /t 3 /nobreak >nul
start "" python -m streamlit run app.py --server.port 8501

echo.
echo Both interfaces have been started!
echo Admin Dashboard: http://localhost:8502
echo Client Chat UI: http://localhost:8501
echo.
echo Close this window to stop the background terminal if needed.
pause
