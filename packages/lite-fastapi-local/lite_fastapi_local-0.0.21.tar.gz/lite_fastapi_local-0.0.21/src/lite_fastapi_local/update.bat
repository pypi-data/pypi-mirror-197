@REM @echo off
FOR /F "tokens=5 delims= " %%P IN ('netstat -ano ^| findstr :8000') DO TaskKill.exe /PID %%P /F

pip install --upgrade --index-url https://test.pypi.org/simple/ --no-deps lite_fastapi_local

python fastapi_local_test.py
