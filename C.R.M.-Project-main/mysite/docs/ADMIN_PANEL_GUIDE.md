# CRM Admin Panel - User Management Guide

## Overview
A comprehensive admin panel for superuser with advanced user management, role-based access control, and master data management.

---

## 🔐 Accessing the Admin Panel

1. **URL**: `http://localhost:8000/admin/`
2. **Login**: Use your superuser credentials
   - If no superuser exists, create one:
     ```bash
     python manage.py createsuperuser
     ```

---

## 📋 Features

### 1. **User Management** (Admin Panel)

#### **Key Capabilities:**
- ✅ User creation with roles (Admin, Sales Head, Sales Executive, etc.)
- ✅ Role-based permissions
- ✅ Password & login control
- ✅ Territory / Zone mapping
- ✅ Department & designation assignment
- ✅ Inline editing of user profiles and employee details

#### **User Roles:**
| Role | Description | Permissions |
|------|-------------|-------------|
| **Admin** | Full system access | View/Edit all data, User management |
| **Manager** | Department manager | View department data, Approve visits |
| **Sales Head** | Regional sales head | View region data, Approve team visits |
| **Sales Executive** | Field sales executive | Create prospects/visits, View own data |
| **Sales Representative** | Entry-level sales rep | Create visits, View assigned prospects |

#### **Creating a New User:**
1. Go to **Users** section in admin panel
2. Click **"Add User"**
3. Fill in basic credentials (username, password)
4. Save and continue editing
5. Fill in **Personal Info** (name, email)
6. Set **Permissions** (Active, Staff, Superuser, Groups)
7. Fill **User Profile** inline section (phone, DOB, bio)
8. Fill **Sales Employee Profile** inline section:
   - Employee ID (unique)
   - Role (Admin/Manager/Sales Head/Executive/Rep)
   - Department
   - Designation
   - Territory/Zone
   - Region
   - Reporting Manager
   - Mobile number
   - Active status
   - Joining date

#### **Bulk Actions:**
- ✓ Activate/Deactivate multiple users
- ✓ Grant/Remove staff access
- ✓ Export user lists

---

### 2. **Department Master**

Manage organizational departments.

#### **Features:**
- Department code and name
- Description
- Active/Inactive status
- Employee count display
- Timestamp tracking

#### **Bulk Actions:**
- Activate/Deactivate departments

#### **Fields:**
- **Name**: Full department name (e.g., "Sales & Marketing")
- **Code**: Short code (e.g., "SM", "HR")
- **Description**: Department purpose/responsibilities
- **Is Active**: Enable/disable department

---

### 3. **Designation Master**

Manage job titles and positions.

#### **Features:**
- Designation code and title
- Department linkage
- Hierarchy level (1=Top, higher=Lower)
- Employee count
- Active/Inactive status

#### **Bulk Actions:**
- Activate/Deactivate designations

#### **Fields:**
- **Title**: Job title (e.g., "Sales Manager")
- **Code**: Short code (e.g., "SM", "SE")
- **Department**: Link to department
- **Level**: Hierarchy position (1=CEO, 2=VP, 3=Manager, etc.)
- **Description**: Role responsibilities

---

### 4. **Territory Master**

Manage geographical zones and territories.

#### **Features:**
- Hierarchical territory structure
- Zone types (Zone/Region/State/District/City)
- Parent-child relationships
- Employee count per territory
- Active/Inactive status

#### **Bulk Actions:**
- Activate/Deactivate territories

#### **Zone Types:**
- **Zone**: Largest geographical division
- **Region**: Sub-zone division
- **State**: State-level territory
- **District**: District-level territory
- **City**: City-level territory

#### **Example Hierarchy:**
```
North Zone (ZONE)
├── Delhi Region (REGION)
│   ├── Delhi (STATE)
│   │   ├── Central Delhi (DISTRICT)
│   │   │   └── Connaught Place (CITY)
```

---

### 5. **Sales Employee Management**

Enhanced employee management with full organizational mapping.

#### **Display Fields:**
- Employee ID & Full Name
- Role (color-coded badge)
- Department
- Designation
- Territory
- Region
- Reporting Manager
- Mobile
- Active Status (badge)
- Joining Date

#### **Filters:**
- Role
- Department
- Designation
- Territory
- Region
- Active Status
- Joining Date

#### **Bulk Actions:**
- ✓ Activate/Deactivate employees
- 📊 Export employee list

---

### 6. **Prospect/Customer Management**

Manage leads, prospects, and customers.

#### **Features:**
- Type badges (Prospect/Customer/Lead)
- Status tracking with color-coded badges
- Visit count display
- GPS coordinates support
- Assignment to sales employees

#### **Status Flow:**
```
NEW → CONTACTED → QUALIFIED → PROPOSAL → NEGOTIATION → WON/LOST
```

#### **Bulk Actions:**
- ✓ Convert to Customer
- ✓ Mark as Won
- ✗ Mark as Lost

---

### 7. **Visit Log Management**

Track and approve sales visits.

#### **Features:**
- Auto-generated Visit IDs (VST-000001)
- Employee and prospect information
- Meeting agenda and outcomes
- GPS location tracking
- File attachments (visiting cards, photos, documents)
- Approval workflow

#### **Approval Workflow:**
```
PENDING ⏳ → APPROVED ✓ / REJECTED ✗
```

#### **Bulk Actions:**
- ✓ Approve visits (for Sales Head/Manager/Admin)
- ✗ Reject visits
- ✓ Mark as completed

---

## 🎨 Admin Panel Customization

### **Branding:**
- Site Header: "CRM Admin Panel"
- Site Title: "CRM Admin"
- Index Title: "Welcome to CRM Administration"

### **Visual Enhancements:**
- Color-coded role badges
- Status indicators
- Employee/Visit counters
- Hierarchical displays
- Inline editing

---

## 🔧 Setup Instructions

### **1. Run Migrations:**
```bash
python manage.py migrate
```

### **2. Create Superuser:**
```bash
python manage.py createsuperuser
```

### **3. Access Admin Panel:**
```
http://localhost:8000/admin/
```

### **4. Initial Setup Order:**

1. **Create Departments**
   - Sales & Marketing
   - Operations
   - Finance
   - HR

2. **Create Designations**
   - CEO (Level 1)
   - VP Sales (Level 2)
   - Sales Manager (Level 3)
   - Sales Executive (Level 4)
   - Sales Representative (Level 5)

3. **Create Territories**
   - North Zone
   - South Zone
   - East Zone
   - West Zone
   - Central Zone

4. **Create Users & Employees**
   - Link users to departments
   - Assign designations
   - Map territories
   - Set reporting hierarchy

5. **Add Prospects/Customers**
   - Assign to sales employees
   - Track with visits

---

## 🛡️ Security & Permissions

### **Superuser (You):**
- Full access to all features
- Can create/edit/delete any data
- Manage user permissions

### **Staff Users:**
- Access to admin panel (if `is_staff=True`)
- Limited by group permissions
- Can be restricted by role

### **Regular Users:**
- No admin panel access
- Use frontend application
- See only assigned data

---

## 📊 Reports & Analytics

### **Available in Admin:**
- Employee counts by department/designation/territory
- Visit counts by prospect
- Approval statistics
- Status distributions

---

## 🚀 Best Practices

1. **User Creation:**
   - Always fill both User and SalesEmployee profiles
   - Use meaningful employee IDs (e.g., EMP001, SM001)
   - Set proper reporting hierarchy

2. **Master Data:**
   - Keep department/designation codes consistent
   - Maintain territory hierarchy properly
   - Mark inactive instead of deleting

3. **Security:**
   - Change default admin password
   - Use strong passwords for all users
   - Regularly review user permissions
   - Deactivate users when they leave

4. **Data Management:**
   - Use bulk actions for efficiency
   - Filter and search before actions
   - Export data regularly for backups

---

## 🆘 Troubleshooting

### **Can't login to admin?**
- Ensure user has `is_staff=True`
- Check username/password
- Create superuser if needed

### **Missing employee profile?**
- User profile auto-creates
- SalesEmployee must be manually added
- Edit user and fill inline sections

### **Can't see certain data?**
- Check user role and permissions
- Verify is_active status
- Contact admin for access

---

## 📞 Support

For issues or feature requests, contact your system administrator.

**Admin Panel Version:** 1.0  
**Last Updated:** November 2025
