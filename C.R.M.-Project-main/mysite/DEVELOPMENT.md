# 🛠️ Development Guide

Complete guide for developers working on the CRM System.

---

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Environment](#development-environment)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Debugging](#debugging)
- [Common Tasks](#common-tasks)
- [Troubleshooting](#troubleshooting)

---

## 🚀 Getting Started

### Quick Setup

```bash
# 1. Obtain project files (download or copy the project folder)
# 2. Navigate to the project directory

# 3. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 4. Install dependencies
pip install -r requirements.txt
pip install -r requirements_mssql.txt
pip install -r requirements-dev.txt

# 5. Configure environment
copy .env.example .env
# Edit .env with your settings

# 6. Create database
python create_mssql_database.py

# 7. Run migrations
python manage.py migrate

# 8. Create superuser
python manage.py createsuperuser

# 9. Start development server
python manage.py runserver
```

### Verify Setup

```bash
# Test connection
python test_connection.py

# Run tests
python manage.py test

# Check code quality
flake8 .
black --check .
```

---

## 💻 Development Environment

### Required Tools

1. **Python 3.11+**
   - Download: https://www.python.org/downloads/

2. **MS SQL Server 2019+**
   - Express Edition (free): https://www.microsoft.com/sql-server/sql-server-downloads
   - SQL Server Management Studio (SSMS)

3. **ODBC Driver**
   - Driver 17 or 18 for SQL Server
   - https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

4. *(Optional)* Version control system of your choice

### Recommended IDE Setup

#### **Visual Studio Code**

Install extensions:
```json
{
  "recommendations": [
    "ms-python.python",
    "ms-python.vscode-pylance",
    "ms-python.black-formatter",
    "ms-mssql.mssql",
    "batisteo.vscode-django",
    "wholroyd.jinja",
    "ms-azuretools.vscode-docker"
  ]
}
```

Settings (`.vscode/settings.json`):
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "100"],
  "editor.formatOnSave": true,
  "files.exclude": {
    "**/__pycache__": true,
    "**/*.pyc": true
  }
}
```

#### **PyCharm**

1. Open project
2. Configure Python interpreter (venv)
3. Enable Django support:
   - Settings → Languages & Frameworks → Django
   - Enable Django support
   - Django project root: (project path)
   - Settings: mysite/settings.py
   - Manage script: manage.py

### Environment Variables

Create `.env` file:

```env
# Database
DB_ENGINE=mssql
DB_NAME=crm_database_dev  # Use separate DB for development
DB_HOST=localhost
DB_PORT=1433
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_USER=  # Empty for Windows Auth
DB_PASSWORD=  # Empty for Windows Auth

# Django
SECRET_KEY=your-dev-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Email (Optional for development)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

## 📁 Project Structure

```
crm-system/
├── docs/                       # Documentation
│   ├── admin-guide.md
│   ├── api-docs.md
│   └── ...
│
├── mysite/                     # Django project settings
│   ├── __init__.py
│   ├── settings.py            # Main configuration
│   ├── urls.py                # Root URL routing
│   ├── wsgi.py
│   └── asgi.py
│
├── newapp/                     # Main application
│   ├── migrations/            # Database migrations
│   │   ├── 0001_initial.py
│   │   └── ...
│   │
│   ├── templates/             # HTML templates
│   │   └── newapp/
│   │       ├── base.html
│   │       ├── dashboard.html
│   │       └── ...
│   │
│   ├── static/                # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── __init__.py
│   ├── models.py              # Database models (1587 lines)
│   ├── views.py               # View functions
│   ├── forms.py               # Form definitions
│   ├── admin.py               # Admin configuration (1528 lines)
│   ├── urls.py                # App URL patterns
│   ├── context_processors.py # Template context
│   └── tests.py               # Tests
│
├── media/                      # User-uploaded files
├── staticfiles/                # Collected static files
│
├── .env                        # Environment variables (local)
├── .env.example                # Environment template
├── .dockerignore               # Docker ignore rules
├── pyproject.toml              # Python project config
├── Dockerfile                  # Docker image
├── docker-compose.yml          # Docker Compose
├── manage.py                   # Django management
├── requirements.txt            # Core dependencies
├── requirements_mssql.txt      # MS SQL dependencies
├── requirements-dev.txt        # Dev dependencies
├── README.md                   # Main documentation
├── CONTRIBUTING.md             # Contribution guidelines
├── DEVELOPMENT.md              # This file
├── CHANGELOG.md                # Version history
└── LICENSE                     # MIT License
```

---

## 🔄 Development Workflow

1. Set up or activate your virtual environment.
2. Make code changes in the appropriate app or module.
3. Create or update migrations when models change:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
4. Run automated tests to validate changes:
   ```bash
   python manage.py test
   ```
5. Format and lint the codebase to maintain consistency:
   ```bash
   black .
   isort .
   flake8 .
   ```
6. Document noteworthy updates in CHANGELOG.md or your preferred tracking system.

---

## 📝 Code Standards

### Python Style

- **PEP 8** compliant
- **Line length**: 100 characters
- **Indentation**: 4 spaces (no tabs)
- **Quotes**: Single quotes for strings
- **Naming**:
  - Classes: `PascalCase`
  - Functions: `snake_case`
  - Constants: `UPPER_SNAKE_CASE`

### Django Conventions

#### Models

```python
class ServiceCall(models.Model):
    """Service call model with auto-generated service number."""
    
    # Constants
    STATUS_NEW = 'NEW'
    STATUS_ASSIGNED = 'ASSIGNED'
    
    STATUS_CHOICES = [
        (STATUS_NEW, 'New'),
        (STATUS_ASSIGNED, 'Assigned'),
    ]
    
    # Fields (grouped logically)
    service_number = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    
    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Service Call"
        ordering = ['-created_at']
    
    def __str__(self):
        return self.service_number
```

#### Views

```python
@login_required
def service_call_list(request):
    """
    Display list of service calls.
    
    Args:
        request: HTTP request object
        
    Returns:
        Rendered template with service calls
    """
    calls = ServiceCall.objects.filter(
        status='OPEN'
    ).select_related('customer', 'technician')
    
    return render(request, 'newapp/servicecall_list.html', {
        'calls': calls
    })
```

### Documentation

- **Module docstrings**: Describe module purpose
- **Class docstrings**: Describe class and usage
- **Function docstrings**: Use Google style

```python
def calculate_total(items, tax_rate):
    """
    Calculate total with tax.
    
    Args:
        items (QuerySet): Items to calculate
        tax_rate (Decimal): Tax rate as percentage
        
    Returns:
        Decimal: Total amount including tax
        
    Raises:
        ValueError: If tax_rate is negative
        
    Example:
        >>> items = ServiceCallItem.objects.filter(call_id=1)
        >>> total = calculate_total(items, Decimal('18.0'))
        >>> print(total)
        11800.00
    """
    pass
```

---

## 🧪 Testing

### Running Tests

```bash
# All tests
python manage.py test

# Specific app
python manage.py test newapp

# Specific test class
python manage.py test newapp.tests.TestServiceCall

# Specific test method
python manage.py test newapp.tests.TestServiceCall.test_service_number_generation

# With coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Open htmlcov/index.html
```

### Writing Tests

Create `newapp/tests.py` or organize tests in `newapp/tests/` directory:

```python
from django.test import TestCase, Client
from django.contrib.auth.models import User
from decimal import Decimal
from .models import ServiceCall, Customer

class ServiceCallTestCase(TestCase):
    """Test ServiceCall model."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.customer = Customer.objects.create(
            name='Test Customer',
            customer_id='CUST-00001'
        )
    
    def test_create_service_call(self):
        """Test creating a service call."""
        call = ServiceCall.objects.create(
            customer=self.customer,
            service_type='REPAIR',
            created_by=self.user
        )
        self.assertIsNotNone(call.service_number)
        self.assertTrue(call.service_number.startswith('SVC-'))
    
    def test_service_call_str(self):
        """Test string representation."""
        call = ServiceCall.objects.create(
            service_number='SVC-2025-0001',
            customer=self.customer,
            created_by=self.user
        )
        self.assertEqual(str(call), 'SVC-2025-0001')
```

### Test Coverage Goals

- **Minimum**: 80% coverage
- **Models**: 100% of custom methods
- **Views**: All user flows
- **Forms**: All validation logic

---

## 🐛 Debugging

### Django Debug Toolbar

```bash
# Install
pip install django-debug-toolbar

# Add to INSTALLED_APPS in settings.py
INSTALLED_APPS = [
    # ...
    'debug_toolbar',
]

# Add to middleware
MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    # ...
]

# Add to urls.py
import debug_toolbar
urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
] + urlpatterns

# Configure
INTERNAL_IPS = ['127.0.0.1']
```

### Logging

```python
import logging
logger = logging.getLogger(__name__)

def my_view(request):
    logger.debug('Debug message')
    logger.info('Info message')
    logger.warning('Warning message')
    logger.error('Error message')
```

### Django Shell

```bash
# Open Django shell
python manage.py shell

# Test queries
>>> from newapp.models import ServiceCall
>>> calls = ServiceCall.objects.all()
>>> print(calls.count())
```

### Database Queries

```bash
# Show SQL for a queryset
>>> from django.db import connection
>>> calls = ServiceCall.objects.all()
>>> print(calls.query)
```

---

## 🔧 Common Tasks

### Create New Model

```python
# 1. Add model to models.py
class MyModel(models.Model):
    name = models.CharField(max_length=100)

# 2. Create migration
python manage.py makemigrations

# 3. Apply migration
python manage.py migrate

# 4. Register in admin.py
@admin.register(MyModel)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['name']
```

### Create New View

```python
# 1. Add view to views.py
def my_view(request):
    return render(request, 'mytemplate.html')

# 2. Add URL to urls.py
urlpatterns = [
    path('my-url/', views.my_view, name='my_view'),
]

# 3. Create template
# templates/newapp/mytemplate.html
```

### Update Static Files

```bash
# Collect static files
python manage.py collectstatic

# Clear browser cache or use hard refresh (Ctrl+F5)
```

### Create New Migration

```bash
# Auto-detect changes
python manage.py makemigrations

# Create empty migration
python manage.py makemigrations newapp --empty

# Name migration
python manage.py makemigrations newapp --name add_warranty_field
```

### Rollback Migration

```bash
# Show migrations
python manage.py showmigrations

# Rollback to specific migration
python manage.py migrate newapp 0012

# Rollback all migrations for an app
python manage.py migrate newapp zero
```

---

## 🔍 Troubleshooting

### Database Connection Issues

```bash
# Test connection
python test_connection.py

# Check ODBC drivers
python -c "import pyodbc; print(pyodbc.drivers())"

# Check settings
python manage.py check
```

### Migration Issues

```bash
# Check migration status
python manage.py showmigrations

# Make migrations
python manage.py makemigrations

# Fake migration (if already applied manually)
python manage.py migrate --fake newapp 0013

# Squash migrations
python manage.py squashmigrations newapp 0001 0013
```

### Import Errors

```bash
# Verify virtual environment is activated
which python  # Should show venv path

# Reinstall dependencies
pip install -r requirements.txt
```

### Static Files Not Loading

```bash
# Collect static files
python manage.py collectstatic --clear

# Check STATIC_URL and STATIC_ROOT in settings.py

# Hard refresh browser (Ctrl+F5)
```

---

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [MS SQL Server Docs](https://docs.microsoft.com/en-us/sql/)
- [Python Documentation](https://docs.python.org/3/)
- [Git Documentation](https://git-scm.com/doc)

---

## 💬 Getting Help

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Ask questions
- **Email**: dev@yourdomain.com

---

**Happy Coding! 🚀**
