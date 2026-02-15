@echo off
REM Educational Management System - Quick Start Setup
REM Aishwarya Vignan Educational Society
REM Technology Partner: Ensafe Technologies Pvt Ltd

echo.
echo ===============================================================
echo   Educational Management System - Setup Script
echo   Aishwarya Vignan Educational Society
echo ===============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org
    pause
    exit /b 1
)

REM Create virtual environment
echo [1/5] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install requirements
echo [3/5] Installing Python dependencies...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install requirements
    pause
    exit /b 1
)

REM Create upload directories
echo [4/5] Creating upload directories...
if not exist "static\uploads\materials" mkdir static\uploads\materials
if not exist "static\uploads\profiles" mkdir static\uploads\profiles
echo Upload directories created.

REM Display setup complete message
echo.
echo [5/5] Setup complete!
echo.
echo ===============================================================
echo   Next Steps:
echo ===============================================================
echo.
echo 1. Ensure MySQL Server is running
echo    - On Windows: Services > MySQL80 (or similar)
echo    - On Mac: System Preferences > MySQL
echo.
echo 2. Update database credentials in config.py:
echo    MYSQL_HOST = 'localhost'
echo    MYSQL_USER = 'root'
echo    MYSQL_PASSWORD = 'your_password'
echo    MYSQL_DB = 'lms_db'
echo.
echo 3. Initialize database:
echo    python setup_database.py
echo.
echo 4. Start the application:
echo    python app.py
echo.
echo 5. Access the application:
echo    http://localhost:5000
echo.
echo ===============================================================
echo   Default Admin Credentials:
echo ===============================================================
echo   Email: admin@aves.edu
echo   Password: Admin@123456
echo   (Change immediately after first login!)
echo.
echo ===============================================================
echo.
pause
