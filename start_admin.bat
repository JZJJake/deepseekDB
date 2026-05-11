@echo off
chcp 65001 >nul
title 政策问答AI - 启动管理端

echo =========================================
echo 政策问答AI (管理后台) - 依赖检查与启动
echo =========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请确保 Python 3.10+ 已安装并添加到系统环境变量 PATH 中。
    pause
    exit /b
)

REM 检查并安装依赖
echo [信息] 正在检查依赖环境，如果第一次运行可能需要较长时间下载 (大约几百MB)...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

if %errorlevel% neq 0 (
    echo [错误] 依赖安装失败，请检查网络或使用管理员权限运行。
    pause
    exit /b
)

echo [信息] 依赖检查完毕！
echo.

REM 检查 .env 文件是否存在
if not exist ".env" (
    echo [警告] 未检测到 .env 文件，已自动从 .env.example 复制。请务必去编辑 .env 填入你的 DeepSeek API Key！
    copy .env.example .env >nul
)

echo [信息] 正在启动管理端后台网页...
streamlit run admin_app.py --server.port 8502

pause
