-- ========================================
-- MS SQL SERVER DATABASE SETUP SCRIPT
-- Run this in SQL Server Management Studio (SSMS)
-- ========================================

-- Check if database exists and create if not
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'crm_database')
BEGIN
    PRINT 'Creating database: crm_database'
    CREATE DATABASE [crm_database]
    COLLATE SQL_Latin1_General_CP1_CI_AS
    PRINT 'Database created successfully!'
END
ELSE
BEGIN
    PRINT 'Database crm_database already exists'
END
GO

-- Use the database
USE [crm_database]
GO

-- Display database information
SELECT 
    'Database Name' AS Property, DB_NAME() AS Value
UNION ALL
SELECT 
    'Database ID', CAST(DB_ID() AS VARCHAR(10))
UNION ALL
SELECT 
    'Collation', DATABASEPROPERTYEX(DB_NAME(), 'Collation')
UNION ALL
SELECT 
    'Compatibility Level', CAST(DATABASEPROPERTYEX(DB_NAME(), 'CompatibilityLevel') AS VARCHAR(10))
UNION ALL
SELECT 
    'Status', DATABASEPROPERTYEX(DB_NAME(), 'Status')
GO

PRINT ''
PRINT '=========================================='
PRINT 'DATABASE READY!'
PRINT '=========================================='
PRINT 'Database: crm_database'
PRINT 'Status: Ready for Django migrations'
PRINT ''
PRINT 'Next steps:'
PRINT '1. Run in your project: python manage.py migrate'
PRINT '2. Create superuser: python manage.py createsuperuser'
PRINT '3. Start server: python manage.py runserver'
PRINT '=========================================='
GO

-- Optional: Create login and user for SQL Authentication
-- Uncomment these lines if you want to use SQL Authentication instead of Windows Auth

/*
-- Create SQL Server login
IF NOT EXISTS (SELECT name FROM sys.server_principals WHERE name = 'crm_user')
BEGIN
    PRINT 'Creating login: crm_user'
    CREATE LOGIN crm_user WITH PASSWORD = 'YourStrongPassword123!';
    PRINT 'Login created successfully!'
END
GO

-- Create user in the database
USE [crm_database]
GO

IF NOT EXISTS (SELECT name FROM sys.database_principals WHERE name = 'crm_user')
BEGIN
    PRINT 'Creating user: crm_user'
    CREATE USER crm_user FOR LOGIN crm_user;
    PRINT 'User created successfully!'
END
GO

-- Grant db_owner role to the user
ALTER ROLE db_owner ADD MEMBER crm_user;
PRINT 'User granted db_owner permissions'
GO

PRINT ''
PRINT 'SQL Authentication setup complete!'
PRINT 'Username: crm_user'
PRINT 'Password: YourStrongPassword123!'
PRINT ''
PRINT 'Update your Django settings.py:'
PRINT '  USER: crm_user'
PRINT '  PASSWORD: YourStrongPassword123!'
PRINT '  Remove Trusted_Connection from extra_params'
GO
*/
