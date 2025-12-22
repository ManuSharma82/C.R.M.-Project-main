# 🗄️ AUTO-CREATE DATABASE IN SQL SERVER

## 🎯 OVERVIEW

I've created **3 methods** to automatically create the database on your SQL Server!

---

## 🚀 METHOD 1: AUTOMATED BATCH SCRIPT (EASIEST!)

### **One-Click Setup:**

```bash
setup_database.bat
```

This script will:
1. ✅ Check if SQL Server is accessible
2. ✅ Create `crm_database` if it doesn't exist
3. ✅ Run Django migrations
4. ✅ Report success/errors

**Time:** 1 minute  
**Difficulty:** Easy  

---

## 🐍 METHOD 2: PYTHON SCRIPT

### **Run the Python script:**

```bash
python create_mssql_database.py
```

### **What it does:**

1. Connects to SQL Server `master` database
2. Checks if `crm_database` exists
3. Creates it if missing
4. Verifies creation
5. Shows database details

### **Configuration (Edit script if needed):**

```python
# In create_mssql_database.py

SERVER = 'localhost'  # Your SQL Server address
DATABASE = 'crm_database'  # Your database name
DRIVER = 'ODBC Driver 18 for SQL Server'  # Your ODBC driver

# Authentication
USE_WINDOWS_AUTH = True  # True = Windows Auth, False = SQL Auth

# For SQL Authentication (if USE_WINDOWS_AUTH = False):
SQL_USER = 'sa'
SQL_PASSWORD = 'YourPassword123!'
```

### **Then run migrations:**

```bash
python manage.py migrate
```

---

## 📝 METHOD 3: SQL SCRIPT (MANUAL)

### **Open SQL Server Management Studio (SSMS):**

1. Connect to your SQL Server
2. Open `create_database.sql`
3. Click **Execute** (F5)
4. Database will be created automatically

### **Or run this SQL directly:**

```sql
-- Check and create database
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'crm_database')
BEGIN
    CREATE DATABASE [crm_database]
    COLLATE SQL_Latin1_General_CP1_CI_AS
END
GO

USE [crm_database]
GO
```

### **Then run migrations:**

```bash
python manage.py migrate
```

---

## 🔧 CONFIGURATION OPTIONS

### **Windows Authentication (Default):**

**Your settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'crm_database',
        'USER': '',  # Empty for Windows Auth
        'PASSWORD': '',  # Empty for Windows Auth
        'HOST': 'localhost',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'Trusted_Connection=yes;TrustServerCertificate=yes;',
        },
    }
}
```

**Pros:**
- ✅ No password needed
- ✅ More secure
- ✅ Easier for development

**Requirements:**
- Your Windows account must have SQL Server permissions
- May need to run as Administrator

---

### **SQL Authentication (Alternative):**

**1. Uncomment the SQL Authentication section in `create_database.sql`**

**2. Run the SQL script to create login:**
```sql
CREATE LOGIN crm_user WITH PASSWORD = 'YourStrongPassword123!';
CREATE USER crm_user FOR LOGIN crm_user;
ALTER ROLE db_owner ADD MEMBER crm_user;
```

**3. Update settings.py:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'crm_database',
        'USER': 'crm_user',  # Your SQL username
        'PASSWORD': 'YourStrongPassword123!',  # Your SQL password
        'HOST': 'localhost',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes;',  # No Trusted_Connection
        },
    }
}
```

**4. Update create_mssql_database.py:**
```python
USE_WINDOWS_AUTH = False
SQL_USER = 'crm_user'
SQL_PASSWORD = 'YourStrongPassword123!'
```

---

## 📋 COMPLETE WORKFLOW

### **Step-by-Step:**

```bash
# 1. Install required packages
pip install pyodbc mssql-django

# 2. Create database (choose one method):
#    Option A: Automated (recommended)
setup_database.bat

#    Option B: Python script
python create_mssql_database.py
python manage.py migrate

#    Option C: SQL script in SSMS
# Run create_database.sql in SSMS, then:
python manage.py migrate

# 3. Create superuser
python manage.py createsuperuser

# 4. Start server
python manage.py runserver

# 5. Access admin
# http://localhost:8000/admin
```

---

## ⚠️ TROUBLESHOOTING

### **Issue 1: "Cannot connect to SQL Server"**

**Check:**
1. SQL Server is running:
   - Services → SQL Server (MSSQLSERVER) → Status: Running
2. Server name is correct:
   - Default: `localhost` or `.` or `(local)`
   - Named instance: `localhost\SQLEXPRESS`
3. Firewall allows SQL Server (port 1433)

---

### **Issue 2: "Login failed for user"**

**For Windows Authentication:**
```
Solution 1: Run as Administrator
Solution 2: Add your Windows account to SQL Server:
  - SSMS → Security → Logins → New Login
  - Add your Windows account
  - Server Roles: sysadmin
```

**For SQL Authentication:**
```
Solution 1: Enable SQL Server Authentication:
  - SSMS → Server Properties → Security
  - Select "SQL Server and Windows Authentication mode"
  - Restart SQL Server service

Solution 2: Check username/password
  - Verify in create_mssql_database.py
  - Verify in settings.py
```

---

### **Issue 3: "pyodbc module not found"**

```bash
pip install pyodbc
```

If installation fails on Windows:
```bash
# Download and install Visual C++ Redistributable
# https://aka.ms/vs/17/release/vc_redist.x64.exe
```

---

### **Issue 4: "ODBC Driver not found"**

**Download and install:**
- [Microsoft ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

**Then update scripts:**
```python
DRIVER = 'ODBC Driver 18 for SQL Server'  # or 17
```

---

### **Issue 5: "Access denied to create database"**

**Grant permissions:**

```sql
-- In SSMS, run as admin:
USE master
GO

-- For Windows Auth:
ALTER SERVER ROLE sysadmin ADD MEMBER [DOMAIN\YourUsername]
GO

-- For SQL Auth:
ALTER SERVER ROLE sysadmin ADD MEMBER crm_user
GO
```

Or grant specific permission:
```sql
GRANT CREATE DATABASE TO [DOMAIN\YourUsername]
GO
```

---

## 🔍 VERIFY DATABASE CREATION

### **Method 1: Using Python script**
```bash
python test_connection.py
```

### **Method 2: Using Django shell**
```bash
python manage.py dbshell
```

### **Method 3: Using SSMS**
- Refresh Databases folder
- Look for `crm_database`

---

## 📊 DATABASE DETAILS

**Default Configuration:**
- **Name:** crm_database
- **Collation:** SQL_Latin1_General_CP1_CI_AS
- **Recovery Model:** FULL
- **Compatibility Level:** Latest

**To customize, edit:**
- `create_mssql_database.py` - Python script
- `create_database.sql` - SQL script

---

## 🎯 RECOMMENDED APPROACH

**For Development (Windows):**
```
1. Use setup_database.bat (automatic!)
2. Uses Windows Authentication
3. Zero configuration needed
```

**For Production:**
```
1. Create database manually or use SQL script
2. Use SQL Authentication
3. Set strong password
4. Use environment variables for credentials
```

---

## ✅ VERIFICATION CHECKLIST

After running the database creation:

- [ ] Script completed without errors
- [ ] Database `crm_database` exists in SQL Server
- [ ] Can connect from Django (`python test_connection.py`)
- [ ] Migrations run successfully (`python manage.py migrate`)
- [ ] Admin panel accessible (`python manage.py runserver`)

---

## 📁 FILES CREATED

| File | Purpose |
|------|---------|
| `create_mssql_database.py` | Python script to create database |
| `setup_database.bat` | Automated setup (database + migrations) |
| `create_database.sql` | SQL script for SSMS |
| `test_connection.py` | Test database connection |
| `DATABASE_SETUP_GUIDE.md` | This guide |

---

## 🚀 QUICK START

**Easiest way (Windows):**

```bash
# Just run this:
setup_database.bat
```

**Done!** Database created and migrated! 🎉

---

## 💡 TIPS

1. **Always backup** before running scripts on production
2. **Use Windows Authentication** for development (easier)
3. **Use SQL Authentication** for production (better control)
4. **Test connection** before running migrations
5. **Keep credentials secure** - never commit passwords to git

---

## 📞 NEED HELP?

**Common commands:**

```bash
# Check if SQL Server is running
services.msc

# Test connection
python test_connection.py

# Verify database
python manage.py dbshell

# Show migrations
python manage.py showmigrations

# Create superuser
python manage.py createsuperuser
```

---

## 🎊 SUMMARY

You now have **3 automated ways** to create your database:

1. ⚡ **setup_database.bat** - One click, fully automated
2. 🐍 **create_mssql_database.py** - Python script with details
3. 📝 **create_database.sql** - SQL script for SSMS

**All methods:**
- ✅ Check if database exists
- ✅ Create if missing
- ✅ Verify creation
- ✅ Show detailed info
- ✅ Handle errors gracefully

**Choose the method you prefer and get started!** 🚀
