@echo off
cls
echo.
echo ================================================
echo   Backend API - Automatic Setup
echo ================================================
echo.
echo Step 1: Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error: Could not activate virtual environment!
    echo Creating new virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
)
echo.
echo Step 2: Creating necessary directories...
if not exist logs mkdir logs
if not exist media mkdir media
if not exist staticfiles mkdir staticfiles
if not exist static mkdir static
echo.
echo Step 3: Installing dependencies (this may take few minutes)...
pip install --upgrade pip
pip install -r requirements/dev.txt
echo.
echo Step 4: Creating database migrations...
python manage.py makemigrations
python manage.py makemigrations users authentication products orders payments transactions notifications
echo.
echo Step 5: Running migrations...
python manage.py migrate
echo.
echo ================================================
echo   Setup Complete!
echo ================================================
echo.
echo To create admin user, run: python manage.py createsuperuser
echo To start server, run: python manage.py runserver
echo.
echo Do you want to create admin user now? (Y/N)
set /p choice=Enter your choice: 
if /i "%choice%"=="Y" (
    python manage.py createsuperuser
)
echo.
echo Starting development server...
python manage.py runserver
