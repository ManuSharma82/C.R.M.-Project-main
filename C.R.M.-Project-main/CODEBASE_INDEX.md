# 📚 CRM Codebase Index

**Last Updated:** 2025  
**Version:** 1.0.0  
**Framework:** Django 5.2.7  
**Database:** MS SQL Server 2019+

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Directory Structure](#directory-structure)
3. [Core Modules](#core-modules)
4. [Database Models](#database-models)
5. [Views & Controllers](#views--controllers)
6. [Forms](#forms)
7. [Templates](#templates)
8. [URL Routing](#url-routing)
9. [Admin Configuration](#admin-configuration)
10. [Static Files](#static-files)
11. [Configuration Files](#configuration-files)
12. [Documentation](#documentation)

---

## 🎯 Project Overview

This is a comprehensive **Customer Relationship Management (CRM)** system built with Django, designed for managing:
- Customer and prospect relationships
- Sales pipeline (leads, quotations, orders)
- Service call management
- Visit tracking and approval workflows
- Master data management

**Technology Stack:**
- Backend: Django 5.2.7, Python 3.11+
- Database: MS SQL Server 2019+ (ODBC Driver 17)
- Frontend: HTML5, CSS3, JavaScript
- Authentication: Django Auth System

---

## 📁 Directory Structure

```
C.R.M.-Project/
├── mysite/                          # Main project directory
│   ├── manage.py                    # Django management script
│   ├── mysite/                      # Project configuration
│   │   ├── __init__.py
│   │   ├── settings.py              # Django settings (MS SQL config)
│   │   ├── urls.py                  # Root URL configuration
│   │   ├── wsgi.py                  # WSGI configuration
│   │   └── asgi.py                  # ASGI configuration
│   │
│   ├── newapp/                      # Main application
│   │   ├── __init__.py
│   │   ├── apps.py                  # App configuration
│   │   ├── models.py                # Database models (1,816 lines, 30+ models)
│   │   ├── views.py                 # View functions (2,295+ lines)
│   │   ├── forms.py                 # Form definitions (964+ lines)
│   │   ├── admin.py                 # Admin panel config (1,628+ lines)
│   │   ├── urls.py                  # App URL routing
│   │   ├── context_processors.py    # Template context processors
│   │   ├── tests.py                 # Unit tests
│   │   │
│   │   ├── migrations/              # Database migrations
│   │   │   ├── 0001_initial.py
│   │   │   ├── 0002_salesemployee_prospectcustomer_visitlog.py
│   │   │   ├── 0003_department_alter_salesemployee_role_and_more.py
│   │   │   ├── 0004_lead_leadhistory.py
│   │   │   ├── 0005_leadactivity.py
│   │   │   ├── 0006_quotation_quotationactivity_quotationattachment_and_more.py
│   │   │   ├── 0007_salesorder_salesorderactivity_salesorderattachment_and_more.py
│   │   │   ├── 0008_prospectcustomer_customer_id_and_more.py
│   │   │   ├── 0009_auto_20251106_1137.py
│   │   │   ├── 0010_deliverytermsmaster_paymenttermsmaster_taxmaster_and_more.py
│   │   │   ├── 0011_quotation_delivery_terms_master_and_more.py
│   │   │   ├── 0012_servicecall_servicecallattachment_servicecallitem_and_more.py
│   │   │   ├── 0013_remove_servicecallitem_warranty_applicable_and_more.py
│   │   │   ├── 0014_faultcategory_slaconfig_serviceinvoice_spareusage_and_more.py
│   │   │   └── 0015_servicecall_equipment_details.py
│   │   │
│   │   ├── templates/               # HTML templates
│   │   │   └── newapp/
│   │   │       ├── base.html                    # Base template
│   │   │       ├── index.html                   # Home page
│   │   │       ├── signin.html                  # Login page
│   │   │       ├── signup.html                  # Registration page
│   │   │       ├── dashboard.html               # Main dashboard
│   │   │       ├── dashboard_backup.html        # Backup dashboard
│   │   │       │
│   │   │       ├── prospect_form.html           # Customer/Prospect forms
│   │   │       ├── prospect_list.html
│   │   │       ├── prospect_detail.html
│   │   │       │
│   │   │       ├── visit_management.html        # Visit management interface
│   │   │       ├── visit_management_backup.html
│   │   │       ├── visit_form.html
│   │   │       ├── visit_list.html
│   │   │       ├── visit_detail.html
│   │   │       ├── visit_report.html            # Visit reports
│   │   │       │
│   │   │       ├── lead_form.html               # Lead management
│   │   │       ├── lead_list.html
│   │   │       ├── lead_detail.html
│   │   │       │
│   │   │       ├── activity_form.html           # Activity tracking
│   │   │       ├── activity_list.html
│   │   │       ├── activity_detail.html
│   │   │       ├── activity_dashboard.html
│   │   │       │
│   │   │       ├── quotation_form.html          # Quotation management
│   │   │       ├── quotation_list.html
│   │   │       ├── quotation_detail.html
│   │   │       │
│   │   │       ├── salesorder_form.html         # Sales order management
│   │   │       ├── salesorder_list.html
│   │   │       ├── salesorder_detail.html
│   │   │       │
│   │   │       ├── servicecall_form.html        # Service call management
│   │   │       ├── servicecall_list.html
│   │   │       ├── servicecall_detail.html
│   │   │       │
│   │   │       └── includes/
│   │   │           └── navbar.html              # Navigation component
│   │   │
│   │   └── static/                  # Static files
│   │       ├── css/                 # Stylesheets
│   │       ├── js/                  # JavaScript files
│   │       └── images/              # Images
│   │
│   ├── docs/                        # Documentation (23 files)
│   │   ├── ADMIN_FEATURES_SUMMARY.md
│   │   ├── ADMIN_PANEL_GUIDE.md
│   │   ├── ADMIN_VIEW_AS_USER.md
│   │   ├── APPLY_BALANCED_DESIGN.md
│   │   ├── BALANCED_DESIGN_SUMMARY.md
│   │   ├── DATABASE_SETUP_GUIDE.md
│   │   ├── FINAL_SETUP_SUMMARY.md
│   │   ├── LEAD_MANAGEMENT_COMPLETE.md
│   │   ├── LEAD_MANAGEMENT_SYSTEM.md
│   │   ├── MIGRATION_SUMMARY.md
│   │   ├── MSSQL_MIGRATION_GUIDE.md
│   │   ├── MSSQL_QUICK_START.md
│   │   ├── NEW_STRUCTURE.md
│   │   ├── ROLE_BASED_DASHBOARD.md
│   │   ├── SERVICE_CALL_SYSTEM.md
│   │   ├── SERVICE_ITEM_ENHANCEMENT.md
│   │   ├── SETUP_ADMIN.md
│   │   ├── STYLING_FIX_SUMMARY.md
│   │   ├── TEMPLATE_CONVERSION_GUIDE.md
│   │   ├── TEMPLATES_UPDATED.md
│   │   ├── UI_REDESIGN_SUMMARY.md
│   │   ├── USER_ACTIVITY_VIEWER.md
│   │   └── VISUAL_COMPARISON.md
│   │
│   ├── backups/                     # Database backups
│   │   └── crm_database_20251106_220715.bak
│   │
│   ├── README.md                    # Main documentation
│   ├── CHANGELOG.md                 # Version history
│   ├── DEVELOPMENT.md               # Developer guide
│   ├── requirements.txt             # Core dependencies
│   ├── requirements_mssql.txt       # MS SQL dependencies
│   ├── requirements-dev.txt         # Development dependencies
│   ├── .env.example                 # Environment template
│   ├── create_database.sql          # Database creation script
│   ├── setup_database.bat           # Database setup script
│   └── pyproject.toml               # Python project config
│
└── .gitattributes                   # Git configuration

```

---

## 🔧 Core Modules

### 1. **Authentication Module**
**Files:** `views.py`, `forms.py`, `templates/newapp/signin.html`, `signup.html`

**Features:**
- User registration with email validation
- Login with username or email
- Password hashing (PBKDF2)
- Session management
- Logout functionality

**Key Classes:**
- `SignUpView` - User registration
- `SignInView` - User login
- `CustomSignUpForm` - Registration form
- `CustomSignInForm` - Login form

---

### 2. **Customer & Prospect Management**
**Files:** `models.py` (ProspectCustomer), `views.py`, `forms.py`

**Models:**
- `ProspectCustomer` - Customer master (CUST-00001 format)
- Unique customer IDs (auto-generated)
- Status tracking (NEW, CONTACTED, QUALIFIED, etc.)
- Territory assignment
- GPS coordinates support

**Key Views:**
- `ProspectListView` - List all customers
- `ProspectCreateView` - Create new customer
- `ProspectDetailView` - View customer details
- `ProspectUpdateView` - Edit customer

---

### 3. **Visit Management**
**Files:** `models.py` (VisitLog), `views.py`, `templates/newapp/visit_*.html`

**Features:**
- Visit logging with GPS tracking
- Approval workflow (PENDING → APPROVED/REJECTED)
- Visit attachments (photos, documents, visiting cards)
- Visit reports and analytics
- Integration with leads

**Models:**
- `VisitLog` - Visit records (VST-000001 format)

**Key Views:**
- `VisitManagementView` - Main visit interface (tabbed)
- `VisitCreateView` - Log new visit
- `VisitDetailView` - View visit details
- `VisitReportView` - Analytics and reports
- `approve_visit` - Approval action

---

### 4. **Lead Management**
**Files:** `models.py` (Lead, LeadHistory, LeadActivity), `views.py`

**Features:**
- Lead pipeline tracking
- Lead conversion workflow
- Activity tracking
- Progress percentage
- Estimated/Actual value tracking
- Status history

**Models:**
- `Lead` - Lead records (LEAD-000001 format)
- `LeadHistory` - Change tracking
- `LeadActivity` - Activity log (ACT-000001 format)

**Statuses:** NEW → CONTACTED → QUALIFIED → PROPOSAL_SENT → IN_NEGOTIATION → WON/LOST

---

### 5. **Activity Tracking**
**Files:** `models.py` (LeadActivity), `views.py`, `templates/newapp/activity_*.html`

**Features:**
- Follow-up management
- Activity types (CALL, EMAIL, MEETING, VISIT, etc.)
- Scheduled activities
- Overdue tracking
- Attachment support

**Key Views:**
- `ActivityListView` - List activities
- `ActivityDashboardView` - Activity overview
- `ActivityCreateView` - Create activity
- `ActivityDetailView` - View activity

---

### 6. **Quotation Management**
**Files:** `models.py` (Quotation, QuotationItem, QuotationAttachment, QuotationActivity)`, `views.py`

**Features:**
- Multi-line quotations
- Item master integration
- Automatic tax calculations
- Approval workflow
- Quote expiration tracking
- Currency support (INR, USD, EUR, GBP)
- Conversion to sales orders

**Models:**
- `Quotation` - Quote header (QUO-000001 format)
- `QuotationItem` - Line items
- `QuotationAttachment` - File attachments
- `QuotationActivity` - Activity log

**Workflow:** DRAFT → PENDING → APPROVED → SENT → ACCEPTED/REJECTED → CONVERTED

---

### 7. **Sales Order Management**
**Files:** `models.py` (SalesOrder, SalesOrderItem, SalesOrderAttachment, SalesOrderActivity)`, `views.py`

**Features:**
- Order processing
- Quotation-to-order conversion
- Status tracking (DRAFT → APPROVED → CONFIRMED → SHIPPED → DELIVERED)
- Multi-line orders
- Payment and delivery terms
- Activity tracking

**Models:**
- `SalesOrder` - Order header (SO-000001 format)
- `SalesOrderItem` - Line items
- `SalesOrderAttachment` - Attachments
- `SalesOrderActivity` - Activity log

---

### 8. **Service Call Management**
**Files:** `models.py` (ServiceCall, ServiceCallItem, ServiceActivity, ServiceCallAttachment, etc.)`, `views.py`

**Features:**
- Service ticket system (SVC-YYYY-0001 format)
- Technician assignment
- Service types (BREAKDOWN, PREVENTIVE, INSTALLATION, etc.)
- Priority levels (LOW, MEDIUM, HIGH, CRITICAL)
- Parts and labor tracking
- Warranty management
- AMC/CMC contract linking
- Customer feedback
- Time tracking
- Resolution codes

**Models:**
- `ServiceCall` - Service ticket header
- `ServiceCallItem` - Parts/labor charges
- `ServiceActivity` - Activity log
- `ServiceCallAttachment` - Attachments
- `SpareUsage` - Spare parts usage
- `ServiceInvoice` - Billing (SVC-INV-YYYY-0001 format)

**Related Models:**
- `Technician` - Service engineers (TECH-00001)
- `WarrantyRecord` - Warranty tracking (WAR-00001)
- `ServiceContract` - AMC/CMC (AMC-YYYY-NNNNN)
- `FaultCategory` - Fault classification
- `SLAConfig` - SLA configuration

---

### 9. **Master Data Management**
**Files:** `models.py`, `admin.py`

**Master Models:**

#### Organizational Structure
- `Department` - Departments
- `Designation` - Job positions
- `Territory` - Geographic zones (hierarchical)
- `SalesEmployee` - Sales staff profiles

#### Product/Service Masters
- `ItemMaster` - Product/service catalog
- `TaxMaster` - Tax configuration (GST, IGST, etc.)
- `PaymentTermsMaster` - Payment terms
- `DeliveryTermsMaster` - Delivery terms (INCO terms)
- `VisitPurposeMaster` - Visit purpose categories

#### Service Masters
- `FaultCategory` - Fault classification
- `SymptomMaster` - Common symptoms
- `SLAConfig` - SLA configurations
- `ApprovalMatrix` - Approval workflows

---

### 10. **Dashboard**
**Files:** `views.py` (DashboardView), `templates/newapp/dashboard.html`

**Features:**
- Role-based dashboards (Admin vs User)
- Real-time statistics
- Visit metrics
- Lead pipeline
- Quotation/Order summaries
- Service call status
- Upcoming follow-ups
- Recent activities
- API endpoints for dynamic updates

**Dashboard Data:**
- Visits (today, month, total)
- Leads by stage
- Quotations (draft, pending, approved)
- Orders (status breakdown)
- Service calls (open, in progress, completed)
- Activity metrics

---

## 🗄️ Database Models

### Complete Model List (30+ Models)

#### User & Organization
1. `UserProfile` - Extended user profile
2. `Department` - Departments
3. `Designation` - Job positions
4. `Territory` - Geographic zones
5. `SalesEmployee` - Sales staff profiles

#### Customer Management
6. `ProspectCustomer` - Customer master
7. `Lead` - Lead records
8. `LeadHistory` - Lead change tracking
9. `LeadActivity` - Lead activities
10. `VisitLog` - Visit records

#### Sales Management
11. `Quotation` - Quotation headers
12. `QuotationItem` - Quotation line items
13. `QuotationAttachment` - Quote attachments
14. `QuotationActivity` - Quote activity log
15. `SalesOrder` - Sales order headers
16. `SalesOrderItem` - Order line items
17. `SalesOrderAttachment` - Order attachments
18. `SalesOrderActivity` - Order activity log

#### Service Management
19. `Technician` - Service technicians
20. `ServiceContract` - AMC/CMC contracts
21. `WarrantyRecord` - Warranty records
22. `ServiceCall` - Service call headers
23. `ServiceCallItem` - Service line items
24. `ServiceActivity` - Service activities
25. `ServiceCallAttachment` - Service attachments
26. `SpareUsage` - Spare parts usage
27. `ServiceInvoice` - Service invoices

#### Master Data
28. `ItemMaster` - Item/product catalog
29. `TaxMaster` - Tax configuration
30. `PaymentTermsMaster` - Payment terms
31. `DeliveryTermsMaster` - Delivery terms
32. `VisitPurposeMaster` - Visit purposes
33. `ApprovalMatrix` - Approval matrix
34. `FaultCategory` - Fault categories
35. `SymptomMaster` - Symptom master
36. `SLAConfig` - SLA configurations

---

## 📄 Views & Controllers

### Authentication Views
- `IndexView` - Home page
- `SignUpView` - User registration
- `SignInView` - User login
- `logout_view` - User logout

### Dashboard
- `DashboardView` - Main dashboard (role-based)

### Prospect Management
- `ProspectListView` - List prospects
- `ProspectCreateView` - Create prospect
- `ProspectDetailView` - View prospect
- `ProspectUpdateView` - Edit prospect

### Visit Management
- `VisitManagementView` - Main visit interface
- `VisitListView` - List visits
- `VisitCreateView` - Create visit
- `VisitDetailView` - View visit
- `VisitUpdateView` - Edit visit
- `VisitReportView` - Visit reports
- `approve_visit` - Approve visit

### Lead Management
- `LeadListView` - List leads
- `LeadCreateView` - Create lead
- `LeadDetailView` - View lead
- `LeadUpdateView` - Edit lead

### Activity Management
- `ActivityListView` - List activities
- `ActivityDashboardView` - Activity dashboard
- `ActivityCreateView` - Create activity
- `ActivityDetailView` - View activity
- `ActivityUpdateView` - Edit activity

### Quotation Management
- `QuotationListView` - List quotations
- `QuotationCreateView` - Create quotation
- `QuotationDetailView` - View quotation
- `QuotationUpdateView` - Edit quotation
- `quotation_send` - Send quotation
- `quotation_approve` - Approve quotation
- `quotation_reject` - Reject quotation
- `quotation_add_activity` - Add activity
- `quotation_add_attachment` - Add attachment

### Sales Order Management
- `SalesOrderListView` - List orders
- `SalesOrderCreateView` - Create order
- `SalesOrderDetailView` - View order
- `SalesOrderUpdateView` - Edit order
- `salesorder_confirm` - Confirm order
- `salesorder_approve` - Approve order
- `salesorder_reject` - Reject order
- `salesorder_add_activity` - Add activity
- `salesorder_add_attachment` - Add attachment

### Service Call Management
- `ServiceCallListView` - List service calls
- `ServiceCallCreateView` - Create service call
- `ServiceCallDetailView` - View service call
- `ServiceCallUpdateView` - Edit service call

### API Endpoints
- `get_quotation_data` - Get quotation JSON
- `get_item_data` - Get item data
- `search_items` - Search items
- `search_prospects` - Search prospects
- `get_prospect_data` - Get prospect data
- `dashboard_data_api` - Dashboard data API

---

## 📝 Forms

**File:** `newapp/forms.py` (964+ lines)

### Authentication Forms
- `CustomSignUpForm` - User registration
- `CustomSignInForm` - User login

### CRM Forms
- `ProspectCustomerForm` - Customer form
- `VisitLogForm` - Visit form
- `VisitApprovalForm` - Visit approval
- `LeadForm` - Lead form
- `LeadActivityForm` - Activity form

### Sales Forms
- `QuotationForm` - Quotation header
- `QuotationItemFormSet` - Quotation items (inline)
- `QuotationAttachmentForm` - Quote attachment
- `QuotationActivityForm` - Quote activity
- `SalesOrderForm` - Sales order header
- `SalesOrderItemFormSet` - Order items (inline)
- `SalesOrderAttachmentForm` - Order attachment
- `SalesOrderActivityForm` - Order activity

### Service Forms
- `ServiceCallForm` - Service call form
- `ServiceCallItemFormSet` - Service items (inline)
- `ServiceCallAttachmentForm` - Service attachment
- `ServiceCallActivityForm` - Service activity

---

## 🎨 Templates

**Location:** `newapp/templates/newapp/`

### Base Templates
- `base.html` - Base template with navigation
- `index.html` - Home page
- `signin.html` - Login page
- `signup.html` - Registration page

### Dashboard
- `dashboard.html` - Main dashboard
- `dashboard_backup.html` - Backup dashboard

### Prospect Management
- `prospect_list.html` - Customer list
- `prospect_form.html` - Customer form
- `prospect_detail.html` - Customer details

### Visit Management
- `visit_management.html` - Main visit interface (tabbed)
- `visit_list.html` - Visit list
- `visit_form.html` - Visit form
- `visit_detail.html` - Visit details
- `visit_report.html` - Visit reports

### Lead Management
- `lead_list.html` - Lead list
- `lead_form.html` - Lead form
- `lead_detail.html` - Lead details

### Activity Management
- `activity_list.html` - Activity list
- `activity_form.html` - Activity form
- `activity_detail.html` - Activity details
- `activity_dashboard.html` - Activity dashboard

### Sales Management
- `quotation_list.html` - Quotation list
- `quotation_form.html` - Quotation form
- `quotation_detail.html` - Quotation details
- `salesorder_list.html` - Order list
- `salesorder_form.html` - Order form
- `salesorder_detail.html` - Order details

### Service Management
- `servicecall_list.html` - Service call list
- `servicecall_form.html` - Service call form
- `servicecall_detail.html` - Service call details

### Components
- `includes/navbar.html` - Navigation bar

---

## 🔗 URL Routing

### Root URLs (`mysite/urls.py`)
```
/admin/              → Django admin
/                    → newapp URLs
```

### App URLs (`newapp/urls.py`)

#### Authentication
- `/` → Index
- `/signup/` → Sign up
- `/signin/` → Sign in
- `/logout/` → Logout

#### Dashboard
- `/dashboard/` → Dashboard

#### Prospects
- `/prospects/` → List
- `/prospects/create/` → Create
- `/prospects/<id>/` → Detail
- `/prospects/<id>/edit/` → Edit

#### Visits
- `/visits/` → Visit management (main)
- `/visits/create/` → Create
- `/visits/<id>/` → Detail
- `/visits/<id>/edit/` → Edit
- `/visits/<id>/approve/` → Approve
- `/reports/visits/` → Reports

#### Leads
- `/leads/` → List
- `/leads/create/` → Create
- `/leads/<id>/` → Detail
- `/leads/<id>/edit/` → Edit

#### Activities
- `/activities/` → List
- `/activities/dashboard/` → Dashboard
- `/activities/create/` → Create
- `/activities/<id>/` → Detail
- `/activities/<id>/edit/` → Edit

#### Quotations
- `/quotations/` → List
- `/quotations/create/` → Create
- `/quotations/<id>/` → Detail
- `/quotations/<id>/edit/` → Edit
- `/quotations/<id>/send/` → Send
- `/quotations/<id>/approve/` → Approve
- `/quotations/<id>/reject/` → Reject
- `/quotations/<id>/add-activity/` → Add activity
- `/quotations/<id>/add-attachment/` → Add attachment

#### Sales Orders
- `/orders/` → List
- `/orders/create/` → Create
- `/orders/<id>/` → Detail
- `/orders/<id>/edit/` → Edit
- `/orders/<id>/confirm/` → Confirm
- `/orders/<id>/approve/` → Approve
- `/orders/<id>/reject/` → Reject
- `/orders/<id>/add-activity/` → Add activity
- `/orders/<id>/add-attachment/` → Add attachment

#### Service Calls
- `/service-calls/` → List
- `/service-calls/create/` → Create
- `/service-calls/<id>/` → Detail
- `/service-calls/<id>/edit/` → Edit

#### API Endpoints
- `/api/get-quotation/` → Get quotation data
- `/api/get-item/` → Get item data
- `/api/search-items/` → Search items
- `/api/search-prospects/` → Search prospects
- `/api/get-prospect/` → Get prospect data
- `/api/dashboard-data/` → Dashboard data
- `/api/dashboard-updates/` → Dashboard updates (legacy)

---

## ⚙️ Admin Configuration

**File:** `newapp/admin.py` (1,628+ lines)

### Custom Admin Site
- Site header: "CRM Admin Panel"
- Site title: "CRM Admin"
- Index title: "Welcome to CRM Administration"

### Admin Classes (25+)

#### Master Data Admin
- `DepartmentAdmin` - Department management
- `DesignationAdmin` - Designation management
- `TerritoryAdmin` - Territory management
- `SalesEmployeeAdmin` - Sales employee management
- `ItemMasterAdmin` - Item master management
- `TaxMasterAdmin` - Tax master management
- `PaymentTermsMasterAdmin` - Payment terms
- `DeliveryTermsMasterAdmin` - Delivery terms
- `VisitPurposeMasterAdmin` - Visit purposes
- `ApprovalMatrixAdmin` - Approval matrix
- `FaultCategoryAdmin` - Fault categories
- `SymptomMasterAdmin` - Symptoms
- `SLAConfigAdmin` - SLA configuration

#### CRM Admin
- `ProspectCustomerAdmin` - Customer management
- `LeadAdmin` - Lead management
- `LeadHistoryAdmin` - Lead history
- `LeadActivityAdmin` - Lead activities
- `VisitLogAdmin` - Visit management

#### Sales Admin
- `QuotationAdmin` - Quotation management
- `QuotationItemAdmin` - Quote items (inline)
- `SalesOrderAdmin` - Order management
- `SalesOrderItemAdmin` - Order items (inline)

#### Service Admin
- `TechnicianAdmin` - Technician management
- `ServiceContractAdmin` - Service contracts
- `WarrantyRecordAdmin` - Warranty records
- `ServiceCallAdmin` - Service call management
- `ServiceCallItemAdmin` - Service items (inline)
- `ServiceActivityAdmin` - Service activities
- `SpareUsageAdmin` - Spare usage
- `ServiceInvoiceAdmin` - Service invoices

### Admin Features
- Advanced search
- Custom filters
- List display customization
- Inline editing
- Bulk actions
- Color-coded status badges
- Related record counts
- Timestamp tracking

---

## 📂 Static Files

**Location:** `newapp/static/`

### Structure
```
static/
├── css/              # Stylesheets
├── js/               # JavaScript files
└── images/           # Images
```

---

## ⚙️ Configuration Files

### Settings (`mysite/settings.py`)
- **Database:** MS SQL Server (ODBC Driver 17)
- **Secret Key:** Environment variable
- **Debug:** Environment variable
- **Allowed Hosts:** Environment variable
- **Installed Apps:** Django apps + `newapp`
- **Middleware:** Security, CSRF, Auth, Messages
- **Templates:** Django template engine
- **Static Files:** `/static/`
- **Media Files:** `/media/`
- **Login URLs:** Custom redirects

### Environment Variables (`.env`)
```
SECRET_KEY=...
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=crm_database
DB_HOST=LAPTOP-F4S2FA88
DB_PORT=1433
DB_DRIVER=ODBC Driver 17 for SQL Server
DB_USER=
DB_PASSWORD=
```

### Dependencies

#### Core (`requirements.txt`)
- Django 5.2.7
- mssql-django 1.6
- pyodbc 5.3.0
- Pillow 12.0.0
- python-decouple (for .env)

#### MS SQL (`requirements_mssql.txt`)
- MS SQL Server driver dependencies

#### Development (`requirements-dev.txt`)
- Development tools

---

## 📚 Documentation

### Main Documentation
- `README.md` - Complete project documentation
- `CHANGELOG.md` - Version history
- `DEVELOPMENT.md` - Developer guide
- `CODEBASE_INDEX.md` - This file

### Feature Documentation (`docs/`)
1. `ADMIN_FEATURES_SUMMARY.md` - Admin panel features
2. `ADMIN_PANEL_GUIDE.md` - Admin usage guide
3. `ADMIN_VIEW_AS_USER.md` - View-as-user feature
4. `DATABASE_SETUP_GUIDE.md` - Database setup
5. `MSSQL_MIGRATION_GUIDE.md` - MS SQL migration
6. `MSSQL_QUICK_START.md` - Quick start
7. `LEAD_MANAGEMENT_SYSTEM.md` - Lead management
8. `SERVICE_CALL_SYSTEM.md` - Service call system
9. `ROLE_BASED_DASHBOARD.md` - Dashboard guide
10. `NEW_STRUCTURE.md` - Application structure
11. `TEMPLATE_CONVERSION_GUIDE.md` - Template guide
12. `UI_REDESIGN_SUMMARY.md` - UI redesign
13. And more...

---

## 🔑 Key Features

### Auto-Generated IDs
- Customers: `CUST-00001`
- Leads: `LEAD-000001`
- Activities: `ACT-000001`
- Visits: `VST-000001`
- Quotations: `QUO-000001`
- Sales Orders: `SO-000001`
- Service Calls: `SVC-YYYY-0001`
- Service Invoices: `SVC-INV-YYYY-0001`
- Service Contracts: `AMC-YYYY-NNNNN`
- Warranty Records: `WAR-00001`
- Technicians: `TECH-00001`

### Workflow Features
- Visit approval workflow
- Quotation approval workflow
- Sales order approval workflow
- Lead pipeline tracking
- Service call status tracking

### Integration Points
- Item master auto-fill
- Tax calculation automation
- Quotation to order conversion
- Visit to lead conversion
- Warranty/AMC linking

---

## 📊 Code Statistics

- **Total Models:** 30+
- **Database Tables:** 41
- **Lines of Code:** ~10,000+
- **Admin Classes:** 25+
- **Views:** 50+
- **Forms:** 20+
- **Templates:** 30+
- **Migrations:** 15

---

## 🚀 Quick Reference

### Start Development Server
```bash
python manage.py runserver
```

### Create Migrations
```bash
python manage.py makemigrations
```

### Apply Migrations
```bash
python manage.py migrate
```

### Create Superuser
```bash
python manage.py createsuperuser
```

### Run Tests
```bash
python manage.py test
```

### Access Points
- Application: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- Dashboard: http://localhost:8000/dashboard/

---

## 📝 Notes

- **Database:** MS SQL Server 2019+ required
- **ODBC Driver:** ODBC Driver 17 for SQL Server required
- **Python:** Python 3.11+ required
- **Authentication:** Windows Authentication (development) or SQL Authentication (production)

---

**For detailed information, refer to:**
- `README.md` - Complete setup and usage guide
- `docs/` - Feature-specific documentation
- Code comments - Inline documentation

---

*This index was generated automatically. Last updated: 2025*



