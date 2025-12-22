# 🔄 Template Conversion Guide

Quick reference for converting old templates to the new unified design system.

---

## 📋 Conversion Checklist

For each template file:

- [ ] Replace DOCTYPE/HTML with `{% extends 'newapp/base.html' %}`
- [ ] Change CSS link from `crm.css` to `unified.css` (or remove - it's in base)
- [ ] Add `{% block title %}` with page name
- [ ] Wrap content in `{% block content %}`
- [ ] Update class names to match new system
- [ ] Remove `{% include 'navbar.html' %}`
- [ ] Remove closing `</body></html>`
- [ ] Test the page

---

## 🔨 Before & After Pattern

### **Old Template Structure:**
```html
<!DOCTYPE html>
{% load static %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Page Title</title>
    <link rel="stylesheet" href="{% static 'newapp/css/crm.css' %}">
</head>
<body>
    <div class="crm-container">
        {% include 'newapp/includes/navbar.html' %}
        
        <div class="page-header">
            <h1>Page Title</h1>
            <a href="#" class="btn btn-primary">Action</a>
        </div>

        <!-- Your content -->

    </div>
</body>
</html>
```

### **New Template Structure:**
```django
{% extends 'newapp/base.html' %}
{% load static %}

{% block title %}Page Title - CRM System{% endblock %}

{% block content %}
    <div class="page-header">
        <h1>Page Title</h1>
        <div class="page-header-actions">
            <a href="#" class="btn btn-primary">Action</a>
        </div>
    </div>

    <!-- Your content -->

{% endblock %}
```

---

## 🎨 Class Name Updates

### **Buttons:**
```html
<!-- OLD -->
<a href="#" class="btn btn-primary">Button</a>

<!-- NEW (same, no change needed) -->
<a href="#" class="btn btn-primary">Button</a>
```

### **Page Header:**
```html
<!-- OLD -->
<div class="page-header">
    <h1>Title</h1>
    <a href="#" class="btn btn-primary">Action</a>
</div>

<!-- NEW (add wrapper for actions) -->
<div class="page-header">
    <div>
        <h1>Title</h1>
    </div>
    <div class="page-header-actions">
        <a href="#" class="btn btn-primary">Action</a>
    </div>
</div>
```

### **Stats Grid:**
```html
<!-- OLD -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-label">Label</div>
        <div class="stat-number">100</div>
    </div>
</div>

<!-- NEW (same, no change needed) -->
<div class="stats-grid">
    <div class="stat-card">
        <div class="stat-label">Label</div>
        <div class="stat-number">100</div>
    </div>
</div>
```

### **Tables:**
```html
<!-- OLD & NEW (same) -->
<div class="table-container">
    <table class="data-table">
        <thead>
            <tr><th>Column</th></tr>
        </thead>
        <tbody>
            <tr><td>Data</td></tr>
        </tbody>
    </table>
</div>
```

### **Forms:**
```html
<!-- OLD & NEW (mostly same) -->
<div class="form-container">
    <form method="post" class="crm-form">
        {% csrf_token %}
        <div class="form-section">
            <h3>Section Title</h3>
            <div class="form-row">
                <div class="form-group">
                    <label>Field Name</label>
                    <input type="text" name="field" class="form-input">
                </div>
            </div>
        </div>
        <div class="form-actions">
            <button type="submit" class="btn btn-primary">Save</button>
            <a href="#" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
```

### **Badges:**
```html
<!-- OLD & NEW (same) -->
<span class="badge badge-pending">Pending</span>
<span class="badge badge-approved">Approved</span>
<span class="badge badge-status-won">Won</span>
```

---

## 📝 Example Conversions

### **Example 1: signin.html**

**BEFORE:**
```html
<!DOCTYPE html>
{% load static %}
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sign In</title>
    <link rel="stylesheet" href="{% static 'newapp/css/auth.css' %}">
</head>
<body>
    <div class="auth-container">
        <h1>Sign In</h1>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Sign In</button>
        </form>
    </div>
</body>
</html>
```

**AFTER:**
```django
{% extends 'newapp/base.html' %}
{% load static %}

{% block title %}Sign In - CRM System{% endblock %}

{% block content %}
    <div class="form-container" style="max-width: 500px; margin: 50px auto;">
        <h1 style="text-align: center; color: var(--primary-color); margin-bottom: 30px;">Sign In</h1>
        
        <form method="post">
            {% csrf_token %}
            
            {% for field in form %}
                <div class="form-group">
                    <label>{{ field.label }}</label>
                    {{ field }}
                    {% if field.errors %}
                        <span class="error-message">{{ field.errors.0 }}</span>
                    {% endif %}
                </div>
            {% endfor %}
            
            <div class="form-actions">
                <button type="submit" class="btn btn-primary" style="width: 100%;">Sign In</button>
            </div>
        </form>
        
        <p style="text-align: center; margin-top: 20px;">
            Don't have an account? <a href="{% url 'newapp:signup' %}">Sign Up</a>
        </p>
    </div>
{% endblock %}
```

### **Example 2: prospect_form.html**

**Convert this pattern:**
```django
{% extends 'newapp/base.html' %}
{% load static %}

{% block title %}
    {% if form.instance.pk %}Edit{% else %}Add{% endif %} Prospect - CRM System
{% endblock %}

{% block content %}
    <div class="page-header">
        <div>
            <h1>{% if form.instance.pk %}Edit{% else %}Add New{% endif %} Prospect</h1>
        </div>
        <div class="page-header-actions">
            <a href="{% url 'newapp:prospect_list' %}" class="btn btn-secondary">← Back to List</a>
        </div>
    </div>

    <div class="form-container">
        <form method="post" class="crm-form">
            {% csrf_token %}
            
            {% if form.non_field_errors %}
                <div class="alert alert-danger">
                    {{ form.non_field_errors }}
                </div>
            {% endif %}
            
            <div class="form-section">
                <h3>Basic Information</h3>
                <div class="form-row">
                    <!-- Form fields -->
                </div>
            </div>
            
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Save</button>
                <a href="{% url 'newapp:prospect_list' %}" class="btn btn-secondary">Cancel</a>
            </div>
        </form>
    </div>
{% endblock %}
```

---

## 🎯 Common Patterns

### **List Page:**
```django
{% extends 'newapp/base.html' %}

{% block title %}Items List - CRM System{% endblock %}

{% block content %}
    <div class="page-header">
        <h1>Items</h1>
        <div class="page-header-actions">
            <a href="{% url 'app:item_create' %}" class="btn btn-primary">+ Add New</a>
        </div>
    </div>

    <div class="filter-section">
        <form method="get" class="filter-form">
            <!-- Filters -->
        </form>
    </div>

    <div class="table-container">
        <table class="data-table">
            <!-- Table content -->
        </table>
    </div>

    <!-- Pagination if needed -->
{% endblock %}
```

### **Detail Page:**
```django
{% extends 'newapp/base.html' %}

{% block title %}{{ object.name }} - CRM System{% endblock %}

{% block content %}
    <div class="page-header">
        <h1>{{ object.name }}</h1>
        <div class="page-header-actions">
            <a href="{% url 'app:item_edit' object.pk %}" class="btn btn-primary">Edit</a>
            <a href="{% url 'app:item_list' %}" class="btn btn-secondary">Back</a>
        </div>
    </div>

    <div class="detail-card">
        <h2>Details</h2>
        <div class="detail-grid">
            <div class="detail-item">
                <strong>Field Name</strong>
                <span>{{ object.field }}</span>
            </div>
            <!-- More fields -->
        </div>
    </div>
{% endblock %}
```

### **Form Page:**
```django
{% extends 'newapp/base.html' %}

{% block title %}Form - CRM System{% endblock %}

{% block content %}
    <div class="page-header">
        <h1>Form Title</h1>
    </div>

    <div class="form-container">
        <form method="post">
            {% csrf_token %}
            
            <div class="form-section">
                <h3>Section Title</h3>
                <div class="form-row">
                    {% for field in form %}
                        <div class="form-group">
                            <label>{{ field.label }}</label>
                            {{ field }}
                        </div>
                    {% endfor %}
                </div>
            </div>
            
            <div class="form-actions">
                <button type="submit" class="btn btn-primary">Submit</button>
                <a href="#" class="btn btn-secondary">Cancel</a>
            </div>
        </form>
    </div>
{% endblock %}
```

---

## ⚡ Quick Tips

1. **Always extend base.html first**
2. **Use semantic HTML** (h1, h2, section, article)
3. **Keep consistent spacing** (use CSS variables)
4. **Test on mobile** (responsive design included)
5. **Use provided components** (don't create custom styling)
6. **Follow Django Admin colors** for consistency

---

## 🐛 Common Issues

### Issue: "Template not found"
**Solution:** Make sure path is correct: `'newapp/base.html'`

### Issue: "Styles not applying"
**Solution:** Hard refresh browser (Ctrl+F5) to clear cache

### Issue: "Navbar/Header duplicated"
**Solution:** Remove `{% include 'navbar.html' %}` - it's in base.html

### Issue: "Page looks broken"
**Solution:** Make sure you have `{% block content %}` and `{% endblock %}`

---

## ✅ Validation Checklist

After converting a template:

- [ ] Page loads without errors
- [ ] Header and nav appear correctly
- [ ] Content is properly styled
- [ ] Buttons work and look consistent
- [ ] Forms submit properly
- [ ] Tables are readable
- [ ] Mobile view works
- [ ] No duplicate headers/navbars
- [ ] All links work
- [ ] CSS classes match new system

---

## 📞 Need Help?

Check these files for examples:
- `newapp/templates/newapp/dashboard.html`
- `newapp/templates/newapp/prospect_list.html`
- `newapp/templates/newapp/index.html`

CSS Reference:
- `newapp/static/newapp/css/unified.css`

---

**Convert one template at a time and test before moving to the next!**
