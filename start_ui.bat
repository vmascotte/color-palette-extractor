@echo off
REM Simple setup and execution script for Color Palette Extractor UI

where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo Python nao encontrado. Instale o Python 3 e certifique-se de que o comando 'python' esta no PATH.
    pause
    exit /b 1
)

if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt
python web_ui.py

