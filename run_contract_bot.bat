@echo off
setlocal
cd /d %~dp0

REM Prompt the user for new values
set /p OPENAI_API_KEY=Enter your OpenAI API key:
set /p DB_HOST=Enter the database host:
set /p DB_USER=Enter the database user:
set /p DB_PASSWORD=Enter the database password:
set /p DB_DATABASE=Enter the database name:

REM Write the updated values to config.yaml
(
  echo openai_api_key: '%OPENAI_API_KEY%'
  echo database:
  echo   host: %DB_HOST%
  echo   user: %DB_USER%
  echo   password: %DB_PASSWORD%
  echo   database: %DB_DATABASE%
) > config.yaml

start "" venv\Scripts\python.exe app.py
timeout /t 5 /nobreak >nul
start http://127.0.0.1:5000
endlocal
