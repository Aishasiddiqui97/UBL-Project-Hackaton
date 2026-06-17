@echo off
cls
echo.
echo ================================================
echo   Starting Backend Server...
echo ================================================
echo.
echo [1/4] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Could not activate virtual environment!
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.
echo [2/4] Checking required packages...
python -c "import django, rest_framework, whitenoise" 2>nul
if %errorlevel% neq 0 (
    echo Installing missing packages...
    pip install -q whitenoise djangorestframework django
)
echo ✓ All packages ready
echo.
echo [3/4] Checking database...
python manage.py migrate --check >nul 2>&1
if %errorlevel% neq 0 (
    echo Running migrations...
    python manage.py migrate
)
echo ✓ Database ready
echo.
echo [4/4] Starting Django development server...
echo.
echo ================================================
echo   Server URLs:
echo ================================================
echo   API Docs:    http://localhost:8000/api/docs/
echo   Admin Panel: http://localhost:8000/admin/
echo   API Base:    http://localhost:8000/api/
echo ================================================
echo.
echo Press CTRL+C to stop the server
echo.
python manage.py runserver
