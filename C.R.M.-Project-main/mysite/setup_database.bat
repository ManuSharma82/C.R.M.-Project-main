@echo off
REM Automated MS SQL Server Database Setup Script

echo ========================================
echo MS SQL SERVER DATABASE SETUP
echo ========================================
echo.

echo Step 1: Creating database on SQL Server...
python create_mssql_database.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Database creation failed!
    echo Please check the error messages above.
    pause
    exit /b 1
)

echo.
echo Step 2: Running Django migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Migrations failed!
    pause
    exit /b 1
)

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Your database is ready!
echo You can now:
echo   1. Create superuser: python manage.py createsuperuser
echo   2. Start server: python manage.py runserver
echo   3. Access admin: http://localhost:8000/admin
echo.
pause
