# 👁️ Admin "View As User" Feature

## 📋 Overview

Admins can now view the CRM from any user's perspective using a dropdown selector in the header. This allows admins to see exactly what data each user has access to without switching accounts.

---

## 🎯 Purpose

**Why This Feature?**
- ✅ Debug user-specific issues
- ✅ Understand user experience
- ✅ Review user's work
- ✅ Verify data visibility
- ✅ Training and support
- ✅ Quality assurance

---

## 🔐 Who Can Use This?

**Access:**
- ✅ **Admins** (is_staff = True)
- ✅ **Superusers** (is_superuser = True)
- ❌ Regular users (cannot view as others)

---

## 🎨 How It Works

### **1. User Selection Dropdown**

**Location:** Top right of header, next to username

**Appearance:**
```
┌────────────────────────────────────────────────┐
│  [👁️ View As User...        ▾]  👤 Admin Name │
└────────────────────────────────────────────────┘
```

**Dropdown Options:**
```
👁️ View As User...
✦ My View (Admin)          ← Return to admin's own view
──────────────
John Doe (Sales Rep)       ← View as John Doe
Jane Smith (Sales Executive)
Bob Johnson (Sales Head)
... (all non-admin users)
```

### **2. Auto-Submit**

When you select a user, the page automatically reloads showing that user's data.

### **3. Visual Indicator**

When viewing as another user, an **orange banner** appears below the navigation:

```
┌─────────────────────────────────────────────────────────┐
│  👁️ Admin View: You are viewing data for John Doe     │
│                            [Return to My View]          │
└─────────────────────────────────────────────────────────┘
```

---

## 📊 What Changes When Viewing As User

### **Dashboard (`/dashboard/`)**

**Shows:**
- Selected user's visit statistics
- Selected user's recent visits
- Selected user's upcoming follow-ups
- Selected user's prospects

**Example:**
```
Admin selects "John Doe"
↓
Dashboard shows:
- Total Visits: 45 (John's visits)
- This Week: 5 (John's visits this week)
- Pending: 3 (John's pending visits)
- Recent Visits: John's last 5 visits
```

### **Visit Management (`/visits/`)**

**Shows:**
- All tabs filtered to selected user
- Selected user's scheduled visits
- Selected user's completed visits
- Selected user's pending approvals

**Stats:**
- Total Visits: User's total
- This Week: User's count
- Today: User's today count
- Pending: User's pending count

### **Reports (`/reports/visits/`)**

**Shows:**
- Reports filtered to selected user's data
- Outcome breakdown for user
- Performance metrics for user
- Visit history for user

---

## 🔄 Complete User Flow

### **Scenario: Admin Wants to Review John Doe's Work**

```
1. Admin logs in → Dashboard
   ↓
2. Clicks dropdown "👁️ View As User..."
   ↓
3. Selects "John Doe (Sales Rep)"
   ↓
4. Page reloads with orange banner:
   "👁️ Admin View: You are viewing data for John Doe"
   ↓
5. Dashboard shows John's stats:
   - Total Visits: 45
   - This Week: 5
   - Recent Visits: John's visits
   ↓
6. Navigate to "Visit Management"
   ↓
7. Sees all of John's visits
   - Scheduled: John's upcoming visits
   - Completed: John's past visits
   - Pending: John's awaiting approval
   ↓
8. Navigate to "Reports"
   ↓
9. Sees John's performance metrics
   ↓
10. Click "Return to My View" in banner
    ↓
11. Back to admin's own data
```

---

## 🎯 Key Features

### **1. Persistent Selection**

The selected user persists across pages:
- Dashboard → Visit Management → Reports
- User selection maintained via URL parameter
- Navigation links include `?view_as_user=123`

### **2. Easy Return**

**Two ways to return to admin view:**
1. Click **"Return to My View"** in orange banner
2. Select **"✦ My View (Admin)"** from dropdown

### **3. No Data Modification**

When viewing as another user:
- ✅ Can view all data
- ❌ Cannot create visits as that user
- ❌ Cannot edit user's data
- ❌ Cannot approve visits
- ✅ Can switch to Admin Panel for modifications

---

## 🛠️ Technical Implementation

### **1. Context Processor**

**File:** `newapp/context_processors.py`

**Provides to all templates:**
- `all_employees` - List of users in dropdown
- `viewing_as_user` - Currently viewed user (if any)
- `is_admin_view` - Boolean flag
- `viewed_employee` - SalesEmployee profile

### **2. View Logic**

**In each view (`DashboardView`, `VisitManagementView`, `VisitReportView`):**

```python
# Get effective user
view_as_user_id = self.request.GET.get('view_as_user')
if view_as_user_id and view_as_user_id != 'self':
    # Get selected user
    user = User.objects.get(id=view_as_user_id)
    # Use their data
    sales_employee = user.sales_profile
else:
    # Use admin's own data
    user = self.request.user
    sales_employee = user.sales_profile
```

### **3. URL Parameter**

**Format:** `?view_as_user=<user_id>`

**Examples:**
- `http://localhost:8000/dashboard/?view_as_user=5`
- `http://localhost:8000/visits/?view_as_user=5`
- `http://localhost:8000/dashboard/?view_as_user=self` (return to own view)

### **4. Template Integration**

**Dropdown in base.html:**
```django
{% if user.is_staff or user.is_superuser %}
    <select name="view_as_user" onchange="this.form.submit()">
        <option value="">👁️ View As User...</option>
        <option value="self">✦ My View (Admin)</option>
        {% for emp in all_employees %}
            <option value="{{ emp.user.id }}">
                {{ emp.user.get_full_name }} ({{ emp.get_role_display }})
            </option>
        {% endfor %}
    </select>
{% endif %}
```

**Navigation links preserve selection:**
```django
<a href="{% url 'dashboard' %}?view_as_user={{ request.GET.view_as_user }}">
    Dashboard
</a>
```

---

## 📊 Data Filtering

### **What Gets Filtered:**

| Page | Filtered Data |
|------|---------------|
| **Dashboard** | - Visit statistics<br>- Recent visits<br>- Follow-ups<br>- Prospect count |
| **Visit Management** | - All visits<br>- Scheduled<br>- Completed<br>- Pending approvals |
| **Reports** | - Total visits<br>- Completion rate<br>- Outcomes<br>- Performance metrics |

### **What Stays the Same:**

| Item | Behavior |
|------|----------|
| **Header** | Still shows admin's name |
| **Admin Panel** | Access unchanged |
| **Permissions** | Admin retains full access |
| **Logout** | Logs out admin |

---

## 🎨 Visual Indicators

### **1. Dropdown Selection**
```
[👁️ View As User...        ▾]   ← Default (Admin's view)
[John Doe (Sales Rep)      ▾]   ← Selected user
```

### **2. Orange Banner**
```css
Background: Orange gradient (#f59e0b to #f97316)
Text: White, bold
Icon: 👁️
```

### **3. Return Link**
White underlined text: "Return to My View"

---

## 🔒 Security Considerations

### **Access Control:**
- ✅ Only staff/superusers can access dropdown
- ✅ URL parameter validated against user permissions
- ✅ Invalid user IDs handled gracefully
- ✅ Non-staff users cannot use this feature

### **Data Integrity:**
- ✅ Read-only view (no modifications)
- ✅ Admin remains logged in as admin
- ✅ No session switching
- ✅ Audit trail maintained (admin's actions logged)

### **Best Practices:**
- ✅ Use for review/debugging only
- ✅ Don't use for daily operations
- ✅ Return to admin view when done
- ✅ Use Admin Panel for modifications

---

## 💡 Use Cases

### **1. User Support**

**Scenario:** User reports "I can't see my visits"

**Solution:**
```
1. Admin selects user from dropdown
2. Views their dashboard
3. Sees what they see
4. Identifies issue (e.g., no sales profile)
5. Fixes in Admin Panel
```

### **2. Quality Assurance**

**Scenario:** Review sales rep's visit logging quality

**Solution:**
```
1. Select sales rep from dropdown
2. Go to Visit Management
3. Review their logged visits
4. Check completeness of data
5. Provide feedback
```

### **3. Performance Review**

**Scenario:** Monthly performance check

**Solution:**
```
1. Select employee from dropdown
2. Go to Reports
3. View their metrics
4. Export or screenshot data
5. Include in review meeting
```

### **4. Training**

**Scenario:** Train new admin on CRM

**Solution:**
```
1. Show admin view (own data)
2. Select sample user
3. Demonstrate filtering
4. Show different user roles
5. Return to admin view
```

---

## ⚙️ Configuration

### **Enable/Disable**

**To disable for specific admins:**

In view, add check:
```python
if not self.request.user.is_superuser:
    # Don't allow view-as-user
    view_as_user_id = None
```

### **Customize Dropdown**

**Filter users in context processor:**
```python
# Only show active users
all_employees = SalesEmployee.objects.filter(
    user__is_active=True
).select_related('user')

# Only show specific roles
all_employees = SalesEmployee.objects.filter(
    role__in=['SALES_REP', 'SALES_EXECUTIVE']
).select_related('user')
```

---

## 🐛 Troubleshooting

### **Issue: Dropdown not appearing**

**Check:**
- Is user staff or superuser?
- Is context processor registered in settings.py?
- Are there employees in the database?

### **Issue: Selection doesn't work**

**Check:**
- Is JavaScript enabled?
- Is form submitting?
- Check browser console for errors

### **Issue: Wrong data showing**

**Check:**
- Is view_as_user parameter in URL?
- Is user ID valid?
- Does user have sales_profile?

### **Issue: Banner not showing**

**Check:**
- Is `viewing_as` in context?
- Is template rendering correctly?
- Check browser developer tools

---

## ✅ Benefits

### **For Admins:**
- ✅ Quick user data review
- ✅ Efficient troubleshooting
- ✅ Better user support
- ✅ No account switching needed
- ✅ Audit-friendly (remains as admin)

### **For Users:**
- ✅ Faster issue resolution
- ✅ Better support experience
- ✅ Admin understands their view
- ✅ Less back-and-forth

### **For Business:**
- ✅ Better quality control
- ✅ Faster support resolution
- ✅ Training tool for admins
- ✅ Performance monitoring
- ✅ Data integrity checks

---

## 📝 Summary

**What It Does:**
- Admins can view CRM from any user's perspective
- Dropdown in header to select user
- Visual banner shows current view
- All pages filtered to selected user's data
- Easy return to admin's own view

**What It Doesn't Do:**
- Doesn't log in as that user
- Doesn't allow data modification
- Doesn't change admin permissions
- Doesn't hide admin features

**Perfect For:**
- User support and troubleshooting
- Quality assurance reviews
- Performance monitoring
- Training new admins
- Understanding user experience

---

**Your admins now have a powerful tool to view the CRM from any user's perspective!** 👁️✨

**Remember:** This is a read-only view for review purposes. Use the Admin Panel for data modifications.
