# CRM System - Internal Documentation

Complete Customer Relationship Management system for managing customers, leads, sales, quotations, and service operations.

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Running the Application](#running-the-application)
- [Project Structure](#project-structure)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Support](#support)

---

## 🎯 Overview

**Technology Stack:**
- **Framework**: Django 5.2+
- **Language**: Python 3.11+
- **Database**: MS SQL Server 2019+
- **Driver**: ODBC Driver 17 for SQL Server

**Project Statistics:**
- **Models**: 30+
- **Database Tables**: 41
- **Lines of Code**: ~10,000+
- **Admin Classes**: 25+

---

## ✨ Features

### Customer Relationship Management
- 👥 Customer master with unique IDs (CUST-00001)
- 📊 Lead management with pipeline tracking
- 📝 Visit logs and activity tracking
- 📈 Lead conversion workflow

### Sales & Quotations
- 💰 Quotation management (QUO-000001)
- 📦 Sales orders (SO-000001)
- 🔗 Item master integration with auto-fill
- 💵 Automatic tax calculations
- ✅ Approval workflow

### Service Call Management
- 🔧 Service tickets (SVC-2025-0001)
- 👨‍🔧 Technician management
- 📋 Parts & labor tracking
- ⏱️ Service activity time tracking
- 🛡️ Warranty management
- 📝 AMC/CMC contracts
- ⭐ Customer feedback system

### Master Data
- 🏷️ Item master catalog
- 💳 Tax configuration (GST)
- 💰 Payment terms
- 🚚 Delivery terms
- 👥 Organizational structure

### Administration
- 🎨 Modern admin panel
- 📊 Role-based dashboards
- 🔍 Advanced search and filtering
- 📈 Comprehensive reporting

---

## 📦 Prerequisites

### Required Software

1. **Python 3.11 or higher**
   ```bash
   python --version
   ```

2. **MS SQL Server 2019+**
   - SQL Server Express (free) or higher
   - SQL Server Management Studio (SSMS) recommended

3. **ODBC Driver 17 or 18 for SQL Server**
   - Download: [Microsoft ODBC Driver](https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server)

### System Requirements

- **OS**: Windows 10/11, Windows Server 2019+
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk**: 500MB for application + database space

---

## ⚡ Installation

### Step 1: Obtain Project Files

1. Download or copy the project directory to your workstation.
2. Open a terminal or PowerShell window in the project folder.

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate  # Windows
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
pip install -r requirements_mssql.txt
```

### Step 4: Verify ODBC Driver

```bash
# Check installed ODBC drivers
python -c "import pyodbc; print(pyodbc.drivers())"

# Should show: ODBC Driver 17 for SQL Server (or Driver 18)
```

---

## ⚙️ Configuration

### Environment Variables

Create `.env` file in project root:

```bash
# Copy template
copy .env.example .env

# Edit .env with your settings
```

**Example .env configuration:**

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Settings
DB_NAME=crm_database
DB_HOST=LAPTOP-F4S2FA88  # Your SQL Server name
DB_PORT=1433
DB_DRIVER=ODBC Driver 17 for SQL Server

# Windows Authentication (Recommended for Development)
DB_USER=
DB_PASSWORD=

# For SQL Authentication (Production)
# DB_USER=crm_user
# DB_PASSWORD=YourStrongPassword123!
```

### Database Configuration

The project uses `python-decouple` for environment management. Database settings in `mysite/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'mssql',
        'NAME': 'crm_database',
        'HOST': 'LAPTOP-F4S2FA88',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
            'extra_params': 'Trusted_Connection=yes;TrustServerCertificate=yes;',
        },
    }
}
```

---

## 🗄️ Database Setup

### Method 1: Automated Setup (Recommended)

```bash
# Run setup script
setup_database.bat

# This will:
# 1. Create database
# 2. Run migrations
# 3. Show status
```

### Method 2: Manual Setup

```bash
# Step 1: Create database
python create_mssql_database.py

# Step 2: Run migrations
python manage.py migrate

# Step 3: Verify connection
python test_connection.py
```

### Method 3: Using SSMS

1. Open SQL Server Management Studio
2. Connect to your server
3. Run the script: `create_database.sql`
4. Then run: `python manage.py migrate`

### Verify Database

```bash
# Test connection
python test_connection.py

# Should show:
# ✅ Connection successful
# ✅ Database: crm_database
# ✅ Tables: 41
```

---

## 🚀 Running the Application

### Development Server

```bash
# Start development server
python manage.py runserver

# Server will start at:
# http://localhost:8000/

# Admin panel:
# http://localhost:8000/admin/
```

### Create Superuser

```bash
python manage.py createsuperuser

# Enter:
# - Username
# - Email
# - Password
```

### Network Access

```bash
# Allow network access
python manage.py runserver 0.0.0.0:8000

# Update ALLOWED_HOSTS in .env
ALLOWED_HOSTS=localhost,127.0.0.1,your-server-ip
```

---

## 📁 Project Structure

```
crm-system/
├── docs/                          # Documentation (23 files)
│   ├── admin guides
│   ├── feature documentation
│   ├── migration guides
│   └── user guides
│
├── mysite/                        # Django project
│   ├── settings.py               # Project configuration
│   ├── urls.py                   # URL routing
│   ├── wsgi.py                   # WSGI config
│   └── asgi.py                   # ASGI config
│
├── newapp/                        # Main application
│   ├── migrations/               # Database migrations (13 files)
│   ├── templates/                # HTML templates
│   │   └── newapp/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       └── ...
│   ├── static/                   # Static files
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── models.py                 # Database models (1587 lines)
│   ├── admin.py                  # Admin panel config (1528 lines)
│   ├── views.py                  # View functions
│   ├── forms.py                  # Form definitions
│   ├── urls.py                   # App URL routing
│   └── tests.py                  # Tests
│
├── media/                         # User uploads
├── staticfiles/                   # Collected static files
│
├── .env                          # Environment variables (local)
├── .env.example                  # Environment template
├── manage.py                     # Django management
├── requirements.txt              # Core dependencies
├── requirements_mssql.txt        # MS SQL dependencies
├── requirements-dev.txt          # Development dependencies
├── README.md                     # This file
├── DEVELOPMENT.md                # Developer guide
├── QUICKSTART.md                 # Quick start guide
└── CHANGELOG.md                  # Version history
```

---

## 💻 Development

### Development Workflow

1. Set up your development environment (create or activate a virtual environment and install dependencies).
2. Make changes to the application code as needed.
3. Create or update database migrations when models change:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Run automated tests to verify your changes:
   ```bash
   python manage.py test
   ```
5. Format and lint the codebase to maintain consistency:
   ```bash
   black .
   isort .
   flake8 .
   ```

### Code Standards

- **PEP 8** compliant
- **Line length**: 100 characters
- **Formatting**: Use `black` and `isort`
- **Linting**: Use `flake8`
- **Testing**: Write tests for new features

### Common Commands

```bash
# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Collect static files
python manage.py collectstatic
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app
python manage.py test newapp

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

### Writing Tests

Tests should be placed in `newapp/tests.py` or organized in `newapp/tests/` directory.

Example test:

```python
from django.test import TestCase
from newapp.models import ServiceCall

class ServiceCallTestCase(TestCase):
    def test_service_number_generation(self):
        """Test automatic service number generation."""
        call = ServiceCall.objects.create(
            customer=self.customer,
            created_by=self.user
        )
        self.assertIsNotNone(call.service_number)
        self.assertTrue(call.service_number.startswith('SVC-'))
```

---

## 🌐 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in .env
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Set strong `SECRET_KEY`
- [ ] Use SQL Authentication (not Windows Auth)
- [ ] Enable HTTPS
- [ ] Configure static file serving
- [ ] Set up database backups
- [ ] Configure logging
- [ ] Set up monitoring

### Environment Variables for Production

```env
DEBUG=False
SECRET_KEY=<strong-production-secret-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

DB_NAME=crm_production
DB_USER=prod_user
DB_PASSWORD=<strong-password>
DB_HOST=your-sql-server
DB_PORT=1433
```

### Production Server (Gunicorn)

```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn mysite.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
```

### IIS Deployment (Windows Server)

1. Install wfastcgi
   ```bash
   pip install wfastcgi
   wfastcgi-enable
   ```

2. Configure IIS site

3. Set up web.config

4. Configure permissions

See `docs/` for detailed deployment instructions.

---

## 📊 Database Schema

### Core Tables (41 Total)

#### Customer Management
- `newapp_prospectcustomer` - Customer master (CUST-00001)
- `newapp_lead` - Lead tracking (LEAD-00001)
- `newapp_leadhistory` - Lead status history
- `newapp_leadactivity` - Lead activities
- `newapp_visitlog` - Visit records

#### Sales Management
- `newapp_quotation` - Quotation headers (QUO-000001)
- `newapp_quotationitem` - Quotation line items
- `newapp_salesorder` - Sales order headers (SO-000001)
- `newapp_salesorderitem` - Sales order line items

#### Service Management
- `newapp_servicecall` - Service call headers (SVC-YYYY-NNNN)
- `newapp_servicecallitem` - Service items/charges
- `newapp_serviceactivity` - Service activities
- `newapp_technician` - Technician master (TECH-00001)
- `newapp_servicecontract` - AMC/CMC contracts (AMC-YYYY-NNNNN)
- `newapp_warrantyrecord` - Warranty tracking (WAR-00001)

#### Master Data
- `newapp_itemmaster` - Item/product catalog
- `newapp_taxmaster` - Tax configuration
- `newapp_paymenttermsmaster` - Payment terms
- `newapp_deliverytermsmaster` - Delivery terms
- `newapp_department` - Departments
- `newapp_designation` - Designations

---

## 🔍 Troubleshooting

### Database Connection Issues

```bash
# Test connection
python test_connection.py

# Check ODBC drivers
python -c "import pyodbc; print(pyodbc.drivers())"

# Verify settings
python manage.py check
```

### Migration Issues

```bash
# Check migration status
python manage.py showmigrations

# Reset migrations (development only)
python manage.py migrate newapp zero
python manage.py migrate
```

### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --clear

# Hard refresh browser (Ctrl+F5)
```

---

## 📞 Support

### Documentation

- **QUICKSTART.md** - 5-minute setup guide
- **DEVELOPMENT.md** - Comprehensive developer guide
- **CHANGELOG.md** - Version history
- **docs/** - Detailed feature documentation

### Internal Support

- **Technical Lead**: [Name/Email]
- **Development Team**: [Team Email]
- **Database Admin**: [Name/Email]

---

## 📈 Version History

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

**Current Version**: 1.0.0  
**Status**: Production Ready  
**Last Updated**: November 2025

---

## 🔒 Security

- Django authentication and authorization
- CSRF protection enabled
- SQL injection prevention (parameterized queries)
- XSS protection enabled
- Password hashing (PBKDF2)
- Environment variable management
- Role-based access control

---

## ⚡ Quick Reference

### Essential Commands

```bash
# Start server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Test database
python test_connection.py
```

### Access Points

- **Admin Panel**: http://localhost:8000/admin
- **Application**: http://localhost:8000/

---

**For detailed developer information, see [DEVELOPMENT.md](DEVELOPMENT.md)**

**For quick setup, see [QUICKSTART.md](QUICKSTART.md)**
