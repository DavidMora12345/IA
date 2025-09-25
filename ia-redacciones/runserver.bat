\
    @echo off
    setlocal
    cd /d %~dp0
    if not exist .venv (
        py -3.13 -m venv .venv
    )
    call .venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
