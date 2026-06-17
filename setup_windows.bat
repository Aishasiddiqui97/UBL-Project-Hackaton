@echo off
echo ================================
echo Backend Setup Script (Windows)
echo ================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo Error: Python not found! Please install Python 3.12+
    pause
    exit /b 1
)
echo.

echo Creating virtual environment...
python -m venv venv
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Installing dependencies...
pip install -r requirements\dev.txt
echo.

echo Creating necessary directories...
if not exist media mkdir media
if not exist staticfiles mkdir staticfiles
if not exist logs mkdir logs
echo.

echo Running database migrations...
python manage.py makemigrations
python manage.py migrate
echo.

echo Collecting static files...
python manage.py collectstatic --noinput
echo.

echo ================================
echo Setup completed successfully!
echo ================================
echo.
echo Next steps:
echo 1. Create superuser: python manage.py createsuperuser
echo 2. Run server: python manage.py runserver
echo 3. Access API docs: http://localhost:8000/api/docs/
echo 4. Access Admin: http://localhost:8000/admin/
echo.
echo Press any key to create superuser now...
pause

python manage.py createsuperuser
echo.

echo Starting development server...
python manage.py runserver
