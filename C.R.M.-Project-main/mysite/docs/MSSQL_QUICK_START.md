# 🚀 MS SQL SERVER MIGRATION - QUICK START GUIDE

## ✅ GOOD NEWS!

Your `settings.py` already has MS SQL Server configuration prepared! We just need to activate it.

---

## 📦 STEP 1: INSTALL REQUIRED PACKAGES

Run in your terminal:

```bash
# Install MS SQL Server support
pip install -r requirements_mssql.txt

# Or manually:
pip install mssql-django python-decouple
```

**Also Required:** Microsoft ODBC Driver for SQL Server
- Download: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
- Install: **ODBC Driver 18 for SQL Server** (recommended) or **ODBC Driver 17**

---

## 🗄️ STEP 2: CREATE MS SQL SERVER DATABASE

### Option A: Local SQL Server (SSMS)

Open SQL Server Management Studio and run:

```sql
-- Create database
CREATE DATABASE crm_database;
GO

-- Create login
CREATE LOGIN crm_user WITH PASSWORD = 'YourStrongPassword123!';
GO

-- Grant permissions
USE crm_database;
GO

CREATE USER crm_user FOR LOGIN crm_user;
GO

ALTER ROLE db_owner ADD MEMBER crm_user;
GO
```

### Option B: Windows Authentication (Easier for Development)

```sql
-- Just create the database
CREATE DATABASE crm_database;
GO

-- Your Windows account will have access automatically
```

---

## ⚙️ STEP 3: CONFIGURE DATABASE CONNECTION

### Create `.env` file:

Copy `.env.example` to `.env` and update:

```bash
copy .env.example .env
```

Then edit `.env`:

```env
# For SQL Authentication
DB_ENGINE=mssql
DB_NAME=crm_database
DB_USER=crm_user
DB_PASSWORD=YourStrongPassword123!
DB_HOST=localhost
DB_PORT=1433
DB_DRIVER=ODBC Driver 18 for SQL Server

# OR for Windows Authentication (easier)
DB_ENGINE=mssql
DB_NAME=crm_database
DB_USER=
DB_PASSWORD=
DB_HOST=localhost
DB_PORT=1433
DB_DRIVER=ODBC Driver 18 for SQL Server
```

### Update `settings.py`:

Open `mysite\settings.py` and **uncomment the MS SQL Server configuration** (lines 87-101):

**BEFORE:**
```python
# Using SQLite for development (temporary)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# MS SQL Server Configuration (commented out - will use later)
# DATABASES = {
#     'default': {
# ...
```

**AFTER:**
```python
# Using SQLite for development (temporary)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# MS SQL Server Configuration (NOW ACTIVE!)
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('MSSQL_DB', 'crm_database'),
        'USER': os.environ.get('MSSQL_USER', ''),
        'PASSWORD': os.environ.get('MSSQL_PASSWORD', ''),
        'HOST': os.environ.get('MSSQL_HOST', 'localhost'),
        'PORT': os.environ.get('MSSQL_PORT', '1433'),
        'OPTIONS': {
            'driver': os.environ.get('MSSQL_DRIVER', 'ODBC Driver 18 for SQL Server'),
            # Windows Authentication (Integrated Security)
            'extra_params': os.environ.get('MSSQL_EXTRA_PARAMS', 'Trusted_Connection=yes;TrustServerCertificate=yes;'),
        },
    }
}
```

**Important:** If using SQL Authentication (username/password), change the extra_params:
```python
'extra_params': 'TrustServerCertificate=yes;',
```

---

## 📤 STEP 4: EXPORT EXISTING DATA

Run the export script:

```bash
export_sqlite_data.bat
```

This will:
- ✅ Backup your SQLite database to `backups/` folder
- ✅ Export all data to JSON files
- ✅ Create timestamped backups

---

## 🔄 STEP 5: MIGRATE TO MS SQL SERVER

### Method A: Automated (RECOMMENDED)

Run the migration script:

```bash
python migrate_to_mssql.py
```

This script will:
1. Test database connection
2. Run migrations
3. Load data from backups
4. Verify data
5. Create superuser

### Method B: Manual

```bash
# 1. Test connection
python manage.py check

# 2. Run migrations
python manage.py migrate

# 3. Load data (use the latest backup file)
python manage.py loaddata backups\full_data_YYYYMMDD_HHMMSS.json

# 4. Create superuser
python manage.py createsuperuser
```

---

## ✅ STEP 6: VERIFY MIGRATION

```bash
# Start server
python manage.py runserver

# Open admin panel
# http://localhost:8000/admin

# Check:
# - Can login?
# - Can see all data?
# - Can create new records?
# - Can edit records?
```

---

## 🔍 TROUBLESHOOTING

### Issue: "pyodbc.Error: ('01000', '[01000]..."

**Cause:** ODBC Driver not installed or wrong version specified

**Solution:**
1. Install ODBC Driver 18 from Microsoft
2. Update `.env`: `DB_DRIVER=ODBC Driver 18 for SQL Server`
3. Restart your terminal/IDE

---

### Issue: "Login failed for user 'crm_user'"

**Solution Option 1 - Fix SQL Authentication:**
```sql
-- In SSMS, run:
ALTER LOGIN crm_user WITH PASSWORD = 'YourStrongPassword123!';
ALTER LOGIN crm_user ENABLE;

-- Enable SQL Server Authentication:
-- SSMS → Server Properties → Security → SQL Server and Windows Authentication mode
```

**Solution Option 2 - Use Windows Authentication (easier):**
Update `.env`:
```env
DB_USER=
DB_PASSWORD=
```

And settings.py extra_params:
```python
'extra_params': 'Trusted_Connection=yes;TrustServerCertificate=yes;',
```

---

### Issue: "Certificate chain not trusted"

**Solution:**
Add `TrustServerCertificate=yes` to extra_params in settings.py:
```python
'extra_params': 'TrustServerCertificate=yes;',
```

---

### Issue: "Cannot load data - foreign key constraint"

**Solution:**
Load data in order:
```bash
# Find your backup files in backups/ folder
python manage.py loaddata backups\full_data_YYYYMMDD_HHMMSS.json
```

If that fails, export with natural keys when exporting:
```bash
python manage.py dumpdata --natural-foreign --natural-primary > data.json
```

---

## 📊 POST-MIGRATION VERIFICATION

Run this in Django shell:

```bash
python manage.py shell
```

```python
from newapp.models import *
from django.contrib.auth.models import User

# Check counts
print(f"Users: {User.objects.count()}")
print(f"Customers: {ProspectCustomer.objects.count()}")
print(f"Leads: {Lead.objects.count()}")
print(f"Quotations: {Quotation.objects.count()}")
print(f"Sales Orders: {SalesOrder.objects.count()}")
print(f"Service Calls: {ServiceCall.objects.count()}")
print(f"Technicians: {Technician.objects.count()}")

# Test creating a record
customer = ProspectCustomer.objects.first()
print(f"\nFirst customer: {customer}")
```

---

## 🎯 RECOMMENDED WORKFLOW

### For Development:
```python
# Use Windows Authentication (easiest)
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'crm_database',
        'HOST': 'localhost',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'Trusted_Connection=yes;TrustServerCertificate=yes;',
        },
    }
}
```

### For Production:
```python
# Use SQL Authentication with environment variables
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASSWORD'],
        'HOST': os.environ['DB_HOST'],
        'PORT': os.environ.get('DB_PORT', '1433'),
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'Encrypt=yes;TrustServerCertificate=no;',
        },
    }
}
```

---

## 📋 CHECKLIST

- [ ] ODBC Driver 18 installed
- [ ] `mssql-django` package installed
- [ ] MS SQL Server database created
- [ ] `.env` file configured
- [ ] `settings.py` updated (MS SQL uncommented, SQLite commented)
- [ ] SQLite data exported
- [ ] Migrations run successfully
- [ ] Data loaded successfully
- [ ] Superuser created/working
- [ ] Admin panel accessible
- [ ] All models visible in admin
- [ ] Can perform CRUD operations
- [ ] Reports working

---

## 🚀 SUMMARY OF COMMANDS

```bash
# 1. Install packages
pip install -r requirements_mssql.txt

# 2. Export SQLite data
export_sqlite_data.bat

# 3. Update settings.py (uncomment MS SQL config)

# 4. Run migration script
python migrate_to_mssql.py

# 5. Start server
python manage.py runserver

# 6. Test at http://localhost:8000/admin
```

---

## ✅ YOU'RE DONE!

Your CRM is now running on **MS SQL Server**!

All your data, configurations, and features have been migrated:
- ✅ All users and permissions
- ✅ All customers, leads, visits
- ✅ All quotations and sales orders
- ✅ All service calls and activities
- ✅ All master data (items, taxes, terms)
- ✅ All admin panel configurations

Enjoy the power and scalability of MS SQL Server! 🎉
