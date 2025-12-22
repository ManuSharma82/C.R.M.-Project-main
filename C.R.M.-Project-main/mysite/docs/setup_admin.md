# Admin Panel Setup - Quick Start Guide

## ✅ What Has Been Completed

### 1. **New Models Added:**
   - ✅ Department (organizational departments)
   - ✅ Designation (job titles/positions)
   - ✅ Territory (geographical zones)
   - ✅ Enhanced SalesEmployee with new fields

### 2. **Enhanced Admin Panel:**
   - ✅ Custom User Admin with inline profiles
   - ✅ Department Master with employee counts
   - ✅ Designation Master with hierarchy
   - ✅ Territory Master with parent-child structure
   - ✅ Enhanced SalesEmployee admin with badges
   - ✅ Enhanced Prospect admin with actions
   - ✅ Enhanced Visit Log with approval workflow
   - ✅ Color-coded status badges
   - ✅ Bulk actions for all models
   - ✅ Advanced filtering and search

### 3. **Migrations Created:**
   - ✅ Migration file: `newapp/migrations/0003_department_alter_salesemployee_role_and_more.py`

---

## 🚀 Next Steps

### Step 1: Apply Database Migrations
```bash
cd mysite
python manage.py migrate
```

### Step 2: Create Superuser (if not exists)
```bash
python manage.py createsuperuser
```
Enter:
- Username: admin (or your choice)
- Email: your_email@example.com
- Password: (choose a strong password)

### Step 3: Start Development Server
```bash
python manage.py runserver
```

### Step 4: Access Admin Panel
Open browser and go to:
```
http://127.0.0.1:8000/admin/
```

Login with your superuser credentials.

---

## 📋 Initial Data Setup (Recommended)

### 1. Create Departments
Navigate to **Departments** → **Add Department**

Example departments:
- **Sales & Marketing** (Code: SM)
- **Operations** (Code: OPS)
- **Finance** (Code: FIN)
- **Human Resources** (Code: HR)
- **IT Support** (Code: IT)

### 2. Create Designations
Navigate to **Designations** → **Add Designation**

Example designations:
| Title | Code | Department | Level |
|-------|------|------------|-------|
| Chief Executive Officer | CEO | Operations | 1 |
| Vice President Sales | VPS | Sales & Marketing | 2 |
| Sales Manager | SM | Sales & Marketing | 3 |
| Sales Head | SH | Sales & Marketing | 3 |
| Sales Executive | SE | Sales & Marketing | 4 |
| Sales Representative | SR | Sales & Marketing | 5 |

### 3. Create Territories
Navigate to **Territories** → **Add Territory**

Example territories:
```
North Zone (Code: NORTH, Type: Zone, Parent: None)
├── Delhi Region (Code: DELHI-REG, Type: Region, Parent: North Zone)
├── Punjab Region (Code: PB-REG, Type: Region, Parent: North Zone)

South Zone (Code: SOUTH, Type: Zone, Parent: None)
├── Karnataka Region (Code: KA-REG, Type: Region, Parent: South Zone)
├── Tamil Nadu Region (Code: TN-REG, Type: Region, Parent: South Zone)

East Zone (Code: EAST, Type: Zone, Parent: None)
West Zone (Code: WEST, Type: Zone, Parent: None)
Central Zone (Code: CENTRAL, Type: Zone, Parent: None)
```

### 4. Create Users with Employee Profiles
Navigate to **Users** → **Add User**

**Example User Setup:**

**Step 1: Basic User Info**
- Username: john.doe
- Password: (set password)

**Step 2: Personal Info**
- First name: John
- Last name: Doe
- Email: john.doe@company.com

**Step 3: Permissions**
- ✓ Active
- ✓ Staff status (to access admin)
- Groups: (optional)

**Step 4: User Profile (Inline)**
- Phone: +91-9876543210
- Date of Birth: 1990-01-15

**Step 5: Sales Employee Profile (Inline)**
- Employee ID: EMP001
- Role: Sales Executive
- Department: Sales & Marketing
- Designation: Sales Executive
- Territory: Delhi Region
- Region: North
- Reporting to: (select manager)
- Mobile: +91-9876543210
- ✓ Is Active
- Joined Date: 2024-01-01

---

## 🎯 Admin Panel Features Overview

### **User Management Section:**
- 👥 Users (with inline profiles)
- 👤 User Profiles
- 🏢 Sales Employees

### **Master Data Section:**
- 🏛️ Departments
- 📋 Designations
- 🗺️ Territories

### **CRM Section:**
- 💼 Prospects/Customers
- 📝 Visit Logs

### **System Section:**
- 👥 Groups (Django default)
- 🔐 Permissions (Django default)

---

## 🔍 Testing the Admin Panel

### Test 1: User Creation
1. Create a new user
2. Verify inline profiles appear
3. Fill sales employee details
4. Save and check list view

### Test 2: Department/Designation
1. Create departments
2. Create designations linked to departments
3. Check employee count displays

### Test 3: Territory Hierarchy
1. Create parent zone
2. Create child regions
3. Verify parent-child relationship

### Test 4: Employee Assignment
1. Edit existing user
2. Assign department, designation, territory
3. Check filters work properly

### Test 5: Bulk Actions
1. Select multiple employees
2. Test activate/deactivate action
3. Verify changes applied

---

## 🎨 Visual Features You'll See

### Color-Coded Badges:
- **Roles:** Admin (Red), Manager (Orange), Sales Head (Yellow), Executive (Cyan), Rep (Green)
- **Status:** Active (Green), Inactive (Red)
- **Approval:** Pending (Orange), Approved (Green), Rejected (Red)
- **Prospect Status:** Various colors for different stages

### Smart Displays:
- Employee count badges on departments/designations/territories
- Visit count on prospects
- Full name with username below
- Company info with city details

### Inline Editing:
- User profiles within user form
- Sales employee details within user form
- Quick edits without navigating away

---

## 🛠️ Common Admin Tasks

### Adding a New Sales Employee:
1. Admin → Users → Add User
2. Set username & password → Save
3. Edit user (auto-redirected)
4. Fill personal info
5. Fill Sales Employee Profile inline
6. Set department, designation, territory
7. Save

### Assigning Territory to Employee:
1. Admin → Sales Employees
2. Click employee name
3. Select Territory from dropdown
4. Save

### Approving Visits in Bulk:
1. Admin → Visit Logs
2. Filter by Approval Status = Pending
3. Select visits to approve
4. Actions → ✓ Approve selected visits
5. Go

### Deactivating Multiple Users:
1. Admin → Users
2. Select users
3. Actions → Deactivate selected users
4. Go

---

## 📊 Filters and Search

### User Filters:
- Staff status
- Active status
- Date joined
- Groups

### Employee Filters:
- Role
- Department
- Designation
- Territory
- Region
- Active status
- Joining date

### Prospect Filters:
- Type
- Status
- City
- State
- Assigned employee
- Created date

### Visit Log Filters:
- Status
- Approval status
- Outcome type
- Visit date
- Employee department
- Employee region

---

## 🔐 Security Reminders

1. **Change default password** after first login
2. **Use strong passwords** for all admin users
3. **Enable 2FA** if available (future enhancement)
4. **Regular backups** of database
5. **Review permissions** quarterly
6. **Audit user activity** regularly
7. **Deactivate** users immediately when they leave

---

## 📞 Need Help?

### Common Issues:

**Q: Can't access admin panel?**
A: Ensure user has `is_staff=True` checked

**Q: Employee profile not showing?**
A: Click "Save and continue editing" after creating user

**Q: Department count not updating?**
A: Refresh page or re-save the department

**Q: Can't see bulk actions?**
A: Select items first, then choose action from dropdown

---

## ✨ Admin Panel URL

```
http://127.0.0.1:8000/admin/
```

or

```
http://localhost:8000/admin/
```

---

## 🎉 You're All Set!

Your comprehensive admin panel is ready with:
- ✅ User Management
- ✅ Role-based Access Control
- ✅ Department/Designation Masters
- ✅ Territory Mapping
- ✅ Employee Hierarchy
- ✅ Bulk Actions
- ✅ Advanced Filtering
- ✅ Visual Enhancements

**Next:** Run migrations and start exploring! 🚀
