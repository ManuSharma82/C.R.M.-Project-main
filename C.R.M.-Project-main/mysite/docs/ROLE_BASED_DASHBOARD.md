# 📊 Role-Based Dashboard System

## 🎯 Overview

The CRM dashboard now shows different content based on user roles:
- **Admin Dashboard:** Aggregate data across all employees
- **Sales Executive Dashboard:** Individual performance metrics

---

## 🔐 Dashboard Types

### **1. Admin Dashboard**
**Who sees it:** Admin, Managers, Sales Heads (when viewing their own data)

**Content:**

#### **📊 Top Stats (4 Cards):**
- **Visits Today** - All visits logged today
- **Visits This Month** - All visits this month
- **Total Leads** - All prospects in system
- **Conversion Rate** - Overall conversion percentage

#### **📈 Leads by Stage:**
Grid showing count of leads in each stage:
- NEW
- CONTACTED
- QUALIFIED
- PROPOSAL
- NEGOTIATION
- WON
- LOST

#### **👥 Employee Performance (Top 10):**
Table showing:
- Employee Name
- Role
- Total Visits
- Completed Visits (green badge)
- Pending Visits (yellow badge)

Sorted by total visits (highest first)

#### **🔔 Upcoming Follow-ups (Next 7 Days):**
Table showing:
- **Sales Rep** (who owns the follow-up)
- Prospect Name
- Company
- Follow-up Date (yellow badge)
- Last Visit Date

Shows all employees' follow-ups

---

### **2. Sales Executive/Rep Dashboard**
**Who sees it:** Sales Reps, Sales Executives (non-admin users)

**Content:**

#### **📊 Top Stats (4 Cards):**
- **Today's Visits** - My visits today
- **Monthly Visits** - My visits this month
- **Active Leads** - My active leads (with total count)
- **Conversion Rate** - My personal conversion %

#### **📈 My Leads by Stage:**
Grid showing MY leads in each stage:
- NEW
- CONTACTED
- QUALIFIED
- PROPOSAL
- NEGOTIATION
- WON
- LOST

Only shows leads assigned to me

#### **🔔 Upcoming Follow-ups (Next 7 Days):**
Table showing MY follow-ups:
- Prospect Name
- Company
- Follow-up Date (yellow badge)
- Last Visit Date

No "Sales Rep" column (because it's all mine)

#### **📅 My Recent Visits (Last 5):**
Table showing:
- Prospect Name
- Company
- Visit Date & Time
- Status (scheduled/completed badge)
- Approval Status (pending/approved badge)

---

## 🔄 How It Works

### **Role Detection:**

```python
# Admin sees aggregate data if:
is_admin = (user.is_staff or user.is_superuser) and not viewing_as_another_user

# Sales rep sees personal data if:
is_sales_rep = not is_admin and has_sales_profile
```

### **Admin Viewing as User:**

When admin selects a specific user:
```
Admin selects "John Doe" from dropdown
↓
Dashboard shows: John's personal dashboard
(Same as what John would see)
```

---

## 📊 Data Calculations

### **Admin Dashboard Queries:**

```python
# Visits
visits_today = All visits with visit_date=today
visits_month = All visits with visit_date >= month_start
total_visits = All visits

# Leads
total_leads = All prospects
active_leads = Prospects with status in [NEW, CONTACTED, QUALIFIED, PROPOSAL, NEGOTIATION]
leads_by_stage = Group by status, count

# Conversion
converted = Prospects with status='WON'
conversion_rate = (converted / total) * 100

# Employee Performance
For each employee:
  - Total visits count
  - Completed visits (status='COMPLETED')
  - Pending visits (approval_status='PENDING')
Order by: Total visits DESC
Limit: Top 10

# Follow-ups
All visits where:
  - next_follow_up_date >= today
  - next_follow_up_date <= today + 7 days
Order by: next_follow_up_date ASC
Limit: 10
```

### **Sales Rep Dashboard Queries:**

```python
# Visits (filtered by sales_employee)
visits_today = My visits with visit_date=today
visits_month = My visits with visit_date >= month_start
total_visits = All my visits

# Leads (filtered by assigned_to)
total_leads = Prospects assigned to me
active_leads = My prospects with status in [NEW, CONTACTED, ...]
leads_by_stage = My prospects grouped by status

# Conversion (my prospects only)
my_converted = My prospects with status='WON'
conversion_rate = (my_converted / my_total) * 100

# Follow-ups (my visits only)
My visits where:
  - next_follow_up_date >= today
  - next_follow_up_date <= today + 7 days
Order by: next_follow_up_date ASC

# Recent Visits (my visits only)
My visits ordered by date DESC
Limit: 5
```

---

## 🎨 Visual Differences

### **Admin Dashboard:**
```
┌─────────────────────────────────────────────────────┐
│  📊 Dashboard - Admin Overview                      │
└─────────────────────────────────────────────────────┘

┌──────────┬──────────┬──────────┬──────────┐
│ Visits   │ Visits   │ Total    │ Conversion│
│ Today    │ Month    │ Leads    │ Rate      │
│   42     │   156    │   248    │  24.5%    │
└──────────┴──────────┴──────────┴──────────┘

📈 Leads by Stage
┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│ NEW  │CONTACTED│QUALIFIED│PROPOSAL│NEGOTIATION│WON│LOST│
│  85  │   42   │   38    │   24   │    18     │ 28│ 13│
└──────┴──────┴──────┴──────┴──────┴──────┴──────┘

👥 Employee Performance
┌───────────────┬──────────┬───────┬───────────┬─────────┐
│ Employee      │ Role     │ Total │ Completed │ Pending │
├───────────────┼──────────┼───────┼───────────┼─────────┤
│ John Doe      │ Sales Rep│  45   │    38     │    7    │
│ Jane Smith    │ Exec     │  42   │    35     │    7    │
└───────────────┴──────────┴───────┴───────────┴─────────┘

🔔 Upcoming Follow-ups (Shows all employees)
```

### **Sales Rep Dashboard:**
```
┌─────────────────────────────────────────────────────┐
│  📊 Dashboard - My Performance                      │
└─────────────────────────────────────────────────────┘

┌──────────┬──────────┬──────────┬──────────┐
│ Today's  │ Monthly  │ Active   │ Conversion│
│ Visits   │ Visits   │ Leads    │ Rate      │
│    5     │   18     │   12     │  22.5%    │
└──────────┴──────────┴──────────┴──────────┘

📈 My Leads by Stage
┌──────┬──────┬──────┬──────┬──────┬──────┬──────┐
│ NEW  │CONTACTED│QUALIFIED│PROPOSAL│NEGOTIATION│WON│LOST│
│   8  │    3   │    4    │    2   │     1     │  2│  1│
└──────┴──────┴──────┴──────┴──────┴──────┴──────┘

🔔 Upcoming Follow-ups (Only mine)

📅 My Recent Visits (Last 5)
```

---

## 🔄 User Flows

### **Admin Flow:**

```
1. Admin logs in
   ↓
2. Sees "Admin Overview" dashboard
   ↓
3. Views:
   - Company-wide visit counts
   - All leads by stage
   - Employee performance ranking
   - All upcoming follow-ups
   ↓
4. Can select specific employee from dropdown
   ↓
5. Dashboard changes to that employee's view
```

### **Sales Rep Flow:**

```
1. Sales rep logs in
   ↓
2. Sees "My Performance" dashboard
   ↓
3. Views:
   - Personal visit counts
   - Personal leads by stage
   - Personal follow-ups only
   - Recent visits history
   ↓
4. Focuses on individual goals and tasks
```

---

## 📋 Technical Implementation

### **View Logic (views.py):**

```python
class DashboardView:
    def get_context_data(self, **kwargs):
        # Determine if admin view
        is_admin = (user.is_staff) and (not viewing_as_user)
        
        if is_admin:
            # Aggregate queries (all data)
            context['visits_today'] = VisitLog.objects.filter(...)
            context['employee_performance'] = SalesEmployee.objects.annotate(...)
            
        else:
            # Individual queries (filtered by sales_employee)
            context['visits_today'] = VisitLog.objects.filter(
                sales_employee=sales_employee,
                ...
            )
```

### **Template Logic (dashboard.html):**

```django
{% if is_admin %}
    {# Admin Dashboard #}
    <h2>👥 Employee Performance</h2>
    {# Show all employees #}
{% else %}
    {# Sales Rep Dashboard #}
    <h2>📅 My Recent Visits</h2>
    {# Show only my data #}
{% endif %}
```

---

## ✅ Benefits

### **For Admins:**
- ✅ **High-level overview** - See company performance at a glance
- ✅ **Employee monitoring** - Track who's performing well
- ✅ **Resource allocation** - Identify bottlenecks
- ✅ **Follow-up oversight** - Ensure no customer is forgotten
- ✅ **Conversion tracking** - Monitor sales pipeline health

### **For Sales Reps:**
- ✅ **Personal focus** - See only relevant data
- ✅ **Goal tracking** - Monitor individual targets
- ✅ **Task management** - Clear follow-up list
- ✅ **Performance awareness** - Know conversion rate
- ✅ **Less distraction** - No irrelevant company data

### **For Business:**
- ✅ **Role-appropriate data** - Right info for right person
- ✅ **Better decisions** - Admins see big picture
- ✅ **Motivated teams** - Reps track personal progress
- ✅ **Accountability** - Performance is transparent
- ✅ **Efficiency** - Everyone sees what they need

---

## 🎯 Key Metrics

### **Admin Metrics:**
| Metric | Description | Purpose |
|--------|-------------|---------|
| **Visits Today** | All visits logged today | Daily activity level |
| **Visits This Month** | Month-to-date visits | Monthly progress |
| **Total Leads** | All prospects | Pipeline size |
| **Conversion Rate** | % of leads converted | Sales effectiveness |
| **Employee Performance** | Visits by employee | Resource management |
| **Upcoming Follow-ups** | All pending follow-ups | Customer retention |

### **Sales Rep Metrics:**
| Metric | Description | Purpose |
|--------|-------------|---------|
| **Today's Visits** | My visits today | Daily goal tracking |
| **Monthly Visits** | My month-to-date | Personal progress |
| **Active Leads** | My working leads | Current workload |
| **Conversion Rate** | My personal % | Performance evaluation |
| **Pending Follow-ups** | My tasks | Action items |
| **Recent Visits** | My history | Activity log |

---

## 📊 Sample Data

### **Admin Dashboard Sample:**
```
Visits Today: 42
Visits This Month: 156
Total Leads: 248
Conversion Rate: 24.5% (61 converted)

Employee Performance:
1. John Doe - 45 visits (38 completed, 7 pending)
2. Jane Smith - 42 visits (35 completed, 7 pending)
3. Bob Johnson - 38 visits (32 completed, 6 pending)

Upcoming Follow-ups: 23 in next 7 days
```

### **Sales Rep Dashboard Sample:**
```
Today's Visits: 5
Monthly Visits: 18
Active Leads: 12 of 21 total
Conversion Rate: 22.5% (5 converted)

My Leads:
- NEW: 8
- CONTACTED: 3
- QUALIFIED: 4
- WON: 5

Pending Follow-ups: 4 in next 7 days
Recent Visits: 5 logged
```

---

## 🔧 Configuration

### **Customize Admin View:**

To change what admins see, edit `views.py`:

```python
# Show more/fewer employees
context['employee_performance'] = ...[:20]  # Top 20

# Change follow-up window
next_follow_up_date__lte=today + timedelta(days=14)  # 14 days
```

### **Customize Sales Rep View:**

```python
# Show more recent visits
context['recent_visits'] = ...[:10]  # Last 10

# Show different stats
context['this_week_visits'] = VisitLog.objects.filter(
    visit_date__gte=week_ago
).count()
```

---

## 📝 Summary

**Admin Dashboard:**
- Company-wide overview
- All employee performance
- All follow-ups
- Aggregate metrics
- Management tool

**Sales Rep Dashboard:**
- Personal performance
- Individual leads
- My follow-ups only
- Personal metrics
- Task management tool

**Both:**
- Clean, modern design
- Role-appropriate data
- Actionable insights
- Real-time updates
- Easy navigation

---

**Your CRM now has intelligent, role-based dashboards that show the right data to the right people!** 📊✨

**Admins see the forest, Sales reps see the trees!**
