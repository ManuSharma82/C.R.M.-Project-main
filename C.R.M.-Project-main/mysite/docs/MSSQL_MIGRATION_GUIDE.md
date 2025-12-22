# MS SQL SERVER MIGRATION GUIDE

## 📦 STEP 1: INSTALL REQUIRED PACKAGES

Run these commands in your terminal:

```bash
# Install MS SQL Server driver for Django
pip install mssql-django

# Install ODBC driver (if not already installed)
# Download and install Microsoft ODBC Driver for SQL Server from:
# https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

# Verify installation
pip list | findstr mssql
```

---

## 🗄️ STEP 2: CREATE MS SQL SERVER DATABASE

### Option A: Using SQL Server Management Studio (SSMS)
```sql
CREATE DATABASE crm_database;
GO

-- Create login (if needed)
CREATE LOGIN crm_user WITH PASSWORD = 'YourStrongPassword123!';
GO

-- Create user and grant permissions
USE crm_database;
GO

CREATE USER crm_user FOR LOGIN crm_user;
GO

ALTER ROLE db_owner ADD MEMBER crm_user;
GO
```

### Option B: Using Azure SQL Database
- Go to Azure Portal
- Create SQL Database
- Note down: Server name, Database name, Username, Password

---

## ⚙️ STEP 3: UPDATE DJANGO SETTINGS

Update `settings.py`:

```python
# OLD SQLite Configuration (BACKUP THIS!)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

# NEW MS SQL Server Configuration
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'crm_database',  # Your database name
        'USER': 'crm_user',      # Your username
        'PASSWORD': 'YourStrongPassword123!',  # Your password
        'HOST': 'localhost',     # Or your server address (e.g., 'server.database.windows.net' for Azure)
        'PORT': '1433',          # Default MS SQL Server port
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',  # Or 'ODBC Driver 17 for SQL Server'
            'extra_params': 'TrustServerCertificate=yes',  # For local development
        },
    }
}

# Optional: Keep SQLite as backup during migration
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'crm_database',
        'USER': 'crm_user',
        'PASSWORD': 'YourStrongPassword123!',
        'HOST': 'localhost',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes',
        },
    },
    'sqlite_backup': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

---

## 📤 STEP 4: EXPORT DATA FROM SQLite

### Method 1: Using Django's dumpdata (RECOMMENDED)

```bash
# Navigate to project directory
cd c:\Users\CIS\Documents\projects\projects\mysite

# Export all data to JSON
python manage.py dumpdata --natural-foreign --natural-primary --indent 2 > data_backup.json

# Or export specific apps
python manage.py dumpdata newapp --natural-foreign --natural-primary --indent 2 > newapp_data.json
python manage.py dumpdata auth --natural-foreign --natural-primary --indent 2 > auth_data.json
python manage.py dumpdata contenttypes --indent 2 > contenttypes_data.json

# Export excluding sessions (optional, reduces file size)
python manage.py dumpdata --exclude auth.permission --exclude contenttypes --exclude sessions --natural-foreign --natural-primary --indent 2 > data_full.json
```

---

## 🔄 STEP 5: MIGRATE TO MS SQL SERVER

```bash
# 1. Update settings.py with MS SQL Server configuration (from Step 3)

# 2. Test connection
python manage.py check

# 3. Create database schema in MS SQL Server
python manage.py migrate

# 4. Create superuser
python manage.py createsuperuser

# 5. Load data from SQLite backup
python manage.py loaddata data_backup.json

# Or if you split the exports:
python manage.py loaddata contenttypes_data.json
python manage.py loaddata auth_data.json
python manage.py loaddata newapp_data.json
```

---

## ⚠️ COMMON ISSUES & SOLUTIONS

### Issue 1: ODBC Driver Not Found
```
Error: [Microsoft][ODBC Driver Manager] Data source name not found
```

**Solution:**
- Download and install: [Microsoft ODBC Driver 18 for SQL Server](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)
- Update `OPTIONS.driver` in settings.py to match installed version

---

### Issue 2: Connection Timeout
```
Error: Login timeout expired
```

**Solution:**
```python
DATABASES = {
    'default': {
        # ... other settings ...
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes;Connection Timeout=30;',
        },
    }
}
```

---

### Issue 3: SSL Certificate Error
```
Error: SSL Provider: The certificate chain was issued by an authority that is not trusted
```

**Solution:**
Add `TrustServerCertificate=yes` to OPTIONS:
```python
'OPTIONS': {
    'driver': 'ODBC Driver 18 for SQL Server',
    'extra_params': 'TrustServerCertificate=yes',
},
```

---

### Issue 4: Loaddata Errors (Foreign Key Constraints)
```
Error: Could not load contenttypes.ContentType
```

**Solution:**
Load in specific order:
```bash
python manage.py loaddata contenttypes_data.json
python manage.py loaddata auth_data.json
python manage.py loaddata newapp_data.json
```

Or use `--natural-foreign --natural-primary` when dumping.

---

## 🔍 VERIFICATION STEPS

After migration, verify everything works:

```bash
# 1. Check database connection
python manage.py dbshell

# 2. Count records in key tables
python manage.py shell
>>> from newapp.models import ProspectCustomer, Lead, Quotation, SalesOrder, ServiceCall
>>> print(f"Customers: {ProspectCustomer.objects.count()}")
>>> print(f"Leads: {Lead.objects.count()}")
>>> print(f"Quotations: {Quotation.objects.count()}")
>>> print(f"Sales Orders: {SalesOrder.objects.count()}")
>>> print(f"Service Calls: {ServiceCall.objects.count()}")

# 3. Test admin panel
python manage.py runserver
# Navigate to http://localhost:8000/admin
# Verify all models are accessible

# 4. Test key operations
# - Create a new customer
# - Create a new quotation
# - Create a new service call
# - Run reports
```

---

## 📊 MS SQL SERVER SPECIFIC OPTIMIZATIONS

### Add Indexes (Optional but Recommended)

```python
# In models.py, add indexes to frequently queried fields
class ProspectCustomer(models.Model):
    # ... existing fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['customer_id']),
            models.Index(fields=['email']),
            models.Index(fields=['phone']),
            models.Index(fields=['company_name']),
        ]

class ServiceCall(models.Model):
    # ... existing fields ...
    
    class Meta:
        indexes = [
            models.Index(fields=['service_number']),
            models.Index(fields=['status']),
            models.Index(fields=['service_request_date']),
            models.Index(fields=['assigned_technician']),
        ]
```

Then run:
```bash
python manage.py makemigrations
python manage.py migrate
```

---

## 🔐 SECURITY BEST PRACTICES

### Use Environment Variables for Credentials

1. Install python-decouple:
```bash
pip install python-decouple
```

2. Create `.env` file:
```env
DB_ENGINE=mssql
DB_NAME=crm_database
DB_USER=crm_user
DB_PASSWORD=YourStrongPassword123!
DB_HOST=localhost
DB_PORT=1433
```

3. Update settings.py:
```python
from decouple import config

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': 'TrustServerCertificate=yes',
        },
    }
}
```

4. Add `.env` to `.gitignore`

---

## 🎯 RECOMMENDED MIGRATION SEQUENCE

```
1. ✅ BACKUP SQLite database (copy db.sqlite3 to safe location)
2. ✅ Install mssql-django package
3. ✅ Install ODBC Driver for SQL Server
4. ✅ Create MS SQL Server database
5. ✅ Export SQLite data using dumpdata
6. ✅ Update settings.py with MS SQL config
7. ✅ Test connection: python manage.py check
8. ✅ Run migrations: python manage.py migrate
9. ✅ Load data: python manage.py loaddata data_backup.json
10. ✅ Create superuser (if needed)
11. ✅ Verify data in admin panel
12. ✅ Test all functionality
13. ✅ Update production settings
```

---

## 📁 BACKUP STRATEGY

Before starting migration:

```bash
# 1. Backup SQLite database
copy db.sqlite3 db.sqlite3.backup

# 2. Backup entire project
# Create a zip or copy entire folder

# 3. Export data
python manage.py dumpdata > full_backup_$(date +%Y%m%d).json
```

---

## 🚀 PRODUCTION CONSIDERATIONS

### For Production MS SQL Server:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'production_crm',
        'USER': 'crm_prod_user',
        'PASSWORD': config('DB_PASSWORD'),  # From environment variable
        'HOST': 'your-server.database.windows.net',  # Azure or on-prem server
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 18 for SQL Server',
            'extra_params': (
                'Encrypt=yes;'
                'TrustServerCertificate=no;'
                'Connection Timeout=30;'
            ),
        },
    }
}

# Connection pooling (optional)
CONN_MAX_AGE = 600  # 10 minutes
```

---

## ✅ POST-MIGRATION CHECKLIST

- [ ] All tables created successfully
- [ ] All data migrated (verify counts)
- [ ] User authentication works
- [ ] Admin panel accessible
- [ ] All CRUD operations work
- [ ] Foreign key relationships intact
- [ ] Auto-increment fields working
- [ ] File uploads work (if any)
- [ ] Reports generate correctly
- [ ] Performance is acceptable
- [ ] Backup strategy in place

---

## 📞 NEED HELP?

Common commands for troubleshooting:

```bash
# Check current database
python manage.py dbshell

# List all migrations
python manage.py showmigrations

# Check for migration issues
python manage.py migrate --plan

# Create new superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test
```
