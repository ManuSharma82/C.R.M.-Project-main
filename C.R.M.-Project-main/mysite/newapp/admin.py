from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from django.utils.html import format_html
from django.db.models import Count
from .models import (
    SpareUsage, ServiceInvoice, FaultCategory, SymptomMaster, SLAConfig,
    UserProfile, SalesEmployee, ProspectCustomer, VisitLog,
    Department, Designation, Territory, Lead, LeadHistory, LeadActivity,
    Quotation, QuotationItem, QuotationAttachment, QuotationActivity,
    SalesOrder, SalesOrderItem, SalesOrderAttachment, SalesOrderActivity,
    ItemMaster, TaxMaster, PaymentTermsMaster, DeliveryTermsMaster,
    VisitPurposeMaster, ApprovalMatrix,
    Technician, ServiceContract, WarrantyRecord, ServiceCall, ServiceCallItem,
    ServiceActivity, ServiceCallAttachment
)

# Register your models here.

# Customize Admin Site
admin.site.site_header = "CRM Admin Panel"
admin.site.site_title = "CRM Admin"
admin.site.index_title = "Welcome to CRM Administration"


# ==========================
# MASTER DATA ADMIN PANELS
# ==========================

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'employee_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Department Information', {
            'fields': ('name', 'code', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def employee_count(self, obj):
        count = obj.employees.count()
        return format_html(
            '<span style="background-color: #007bff; color: white; padding: 2px 8px; border-radius: 3px;">{}</span>',
            count
        )
    employee_count.short_description = 'Employees'
    
    actions = ['activate_departments', 'deactivate_departments']
    
    def activate_departments(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} department(s) activated successfully.")
    activate_departments.short_description = "Activate selected departments"
    
    def deactivate_departments(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} department(s) deactivated successfully.")
    deactivate_departments.short_description = "Deactivate selected departments"


@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'department', 'level', 'employee_count', 'is_active', 'created_at')
    list_filter = ('department', 'level', 'is_active', 'created_at')
    search_fields = ('title', 'code', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Designation Information', {
            'fields': ('title', 'code', 'department', 'level', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def employee_count(self, obj):
        count = obj.employees.count()
        return format_html(
            '<span style="background-color: #28a745; color: white; padding: 2px 8px; border-radius: 3px;">{}</span>',
            count
        )
    employee_count.short_description = 'Employees'
    
    actions = ['activate_designations', 'deactivate_designations']
    
    def activate_designations(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} designation(s) activated successfully.")
    activate_designations.short_description = "Activate selected designations"
    
    def deactivate_designations(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} designation(s) deactivated successfully.")
    deactivate_designations.short_description = "Deactivate selected designations"


@admin.register(Territory)
class TerritoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'zone_type', 'parent', 'employee_count', 'is_active', 'created_at')
    list_filter = ('zone_type', 'is_active', 'created_at')
    search_fields = ('name', 'code', 'description')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Territory Information', {
            'fields': ('name', 'code', 'zone_type', 'parent', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def employee_count(self, obj):
        count = obj.employees.count()
        return format_html(
            '<span style="background-color: #6f42c1; color: white; padding: 2px 8px; border-radius: 3px;">{}</span>',
            count
        )
    employee_count.short_description = 'Employees'
    
    actions = ['activate_territories', 'deactivate_territories']
    
    def activate_territories(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} territor(y/ies) activated successfully.")
    activate_territories.short_description = "Activate selected territories"
    
    def deactivate_territories(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} territor(y/ies) deactivated successfully.")
    deactivate_territories.short_description = "Deactivate selected territories"


# ==========================
# USER MANAGEMENT
# ==========================

# Inline for SalesEmployee in User Admin
class SalesEmployeeInline(admin.StackedInline):
    model = SalesEmployee
    can_delete = False
    verbose_name_plural = 'Sales Employee Profile'
    fk_name = 'user'
    fields = ('employee_id', 'role', 'department', 'designation', 'territory', 
              'region', 'reporting_to', 'mobile', 'is_active', 'joined_date')


# Inline for UserProfile in User Admin
class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profile'
    fk_name = 'user'
    fields = ('phone_number', 'date_of_birth', 'bio', 'profile_picture')


# Custom User Admin
class CustomUserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline, SalesEmployeeInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 
                   'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active', 'date_joined', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('-date_joined',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )
    
    def get_role(self, obj):
        try:
            role = obj.sales_profile.role
            colors = {
                'ADMIN': '#dc3545',
                'MANAGER': '#fd7e14',
                'SALES_HEAD': '#ffc107',
                'SALES_EXECUTIVE': '#17a2b8',
                'SALES_REP': '#28a745',
            }
            return format_html(
                '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-weight: bold;">{}</span>',
                colors.get(role, '#6c757d'),
                obj.sales_profile.get_role_display()
            )
        except SalesEmployee.DoesNotExist:
            return format_html('<span style="color: #999;">-</span>')
    get_role.short_description = 'Role'
    
    actions = ['activate_users', 'deactivate_users', 'make_staff', 'remove_staff']
    
    def activate_users(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} user(s) activated successfully.")
    activate_users.short_description = "Activate selected users"
    
    def deactivate_users(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} user(s) deactivated successfully.")
    deactivate_users.short_description = "Deactivate selected users"
    
    def make_staff(self, request, queryset):
        updated = queryset.update(is_staff=True)
        self.message_user(request, f"{updated} user(s) granted staff access.")
    make_staff.short_description = "Grant staff access to selected users"
    
    def remove_staff(self, request, queryset):
        updated = queryset.update(is_staff=False)
        self.message_user(request, f"{updated} user(s) removed from staff.")
    remove_staff.short_description = "Remove staff access from selected users"


# Unregister the default User admin and register the custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Profile Details', {
            'fields': ('bio', 'phone_number', 'date_of_birth', 'profile_picture')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(SalesEmployee)
class SalesEmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'get_full_name', 'role_badge', 'department', 'designation', 
                   'territory', 'region', 'reporting_to', 'mobile', 'status_badge', 'joined_date')
    list_filter = ('role', 'department', 'designation', 'territory', 'region', 'is_active', 'joined_date')
    search_fields = ('employee_id', 'user__username', 'user__first_name', 'user__last_name', 
                    'user__email', 'mobile')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'joined_date'
    list_per_page = 25
    
    fieldsets = (
        ('User Account', {
            'fields': ('user',),
            'description': 'Link to Django user account'
        }),
        ('Employee Information', {
            'fields': ('employee_id', 'mobile', 'joined_date')
        }),
        ('Role & Organization', {
            'fields': ('role', 'department', 'designation', 'territory', 'region'),
            'description': 'Organizational hierarchy and role assignment'
        }),
        ('Reporting Structure', {
            'fields': ('reporting_to',),
            'description': 'Define reporting hierarchy'
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        full_name = obj.user.get_full_name()
        if full_name:
            return format_html('<strong>{}</strong><br><small>{}</small>', 
                             full_name, obj.user.username)
        return obj.user.username
    get_full_name.short_description = 'Name'
    
    def role_badge(self, obj):
        colors = {
            'ADMIN': '#dc3545',
            'MANAGER': '#fd7e14',
            'SALES_HEAD': '#ffc107',
            'SALES_EXECUTIVE': '#17a2b8',
            'SALES_REP': '#28a745',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.role, '#6c757d'),
            obj.get_role_display()
        )
    role_badge.short_description = 'Role'
    
    def status_badge(self, obj):
        if obj.is_active:
            return format_html(
                '<span style="background-color: #28a745; color: white; padding: 3px 10px; border-radius: 3px;">Active</span>'
            )
        return format_html(
            '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px;">Inactive</span>'
        )
    status_badge.short_description = 'Status'
    
    actions = ['activate_employees', 'deactivate_employees', 'assign_to_territory', 'export_employee_list']
    
    def activate_employees(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} employee(s) activated successfully.")
    activate_employees.short_description = "✓ Activate selected employees"
    
    def deactivate_employees(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} employee(s) deactivated successfully.")
    deactivate_employees.short_description = "✗ Deactivate selected employees"
    
    def export_employee_list(self, request, queryset):
        # Simple export action placeholder
        count = queryset.count()
        self.message_user(request, f"{count} employee(s) ready for export (implement CSV/Excel export).")
    export_employee_list.short_description = "📊 Export selected employees"


@admin.register(ProspectCustomer)
class ProspectCustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'name', 'company_name', 'type_badge', 'status_badge', 'phone', 
                   'city', 'assigned_to', 'visit_count', 'created_at')
    list_filter = ('type', 'status', 'city', 'state', 'assigned_to', 'created_at')
    search_fields = ('customer_id', 'name', 'company_name', 'phone', 'email', 'city', 'industry')
    readonly_fields = ('customer_id', 'created_at', 'updated_at', 'created_by')
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Customer Identification', {
            'fields': ('customer_id',)
        }),
        ('Basic Information', {
            'fields': ('name', 'company_name', 'type', 'status', 'industry')
        }),
        ('Contact Details', {
            'fields': ('email', 'phone', 'alternate_phone')
        }),
        ('Address', {
            'fields': ('address', 'city', 'state', 'pincode')
        }),
        ('Location Coordinates', {
            'fields': ('latitude', 'longitude'),
            'classes': ('collapse',),
            'description': 'GPS coordinates for mapping'
        }),
        ('Assignment', {
            'fields': ('assigned_to', 'created_by', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def type_badge(self, obj):
        colors = {
            'PROSPECT': '#17a2b8',
            'CUSTOMER': '#28a745',
            'LEAD': '#ffc107',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.type, '#6c757d'),
            obj.get_type_display()
        )
    type_badge.short_description = 'Type'
    
    def status_badge(self, obj):
        colors = {
            'NEW': '#007bff',
            'CONTACTED': '#17a2b8',
            'QUALIFIED': '#20c997',
            'PROPOSAL': '#ffc107',
            'NEGOTIATION': '#fd7e14',
            'WON': '#28a745',
            'LOST': '#dc3545',
            'INACTIVE': '#6c757d',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def visit_count(self, obj):
        count = obj.visits.count()
        if count > 0:
            return format_html(
                '<span style="background-color: #007bff; color: white; padding: 2px 8px; border-radius: 3px;">{}</span>',
                count
            )
        return '-'
    visit_count.short_description = 'Visits'
    
    actions = ['mark_as_customer', 'mark_as_won', 'mark_as_lost', 'assign_to_employee']
    
    def mark_as_customer(self, request, queryset):
        updated = queryset.update(type='CUSTOMER', status='WON')
        self.message_user(request, f"{updated} prospect(s) marked as customers.")
    mark_as_customer.short_description = "✓ Convert to Customer"
    
    def mark_as_won(self, request, queryset):
        updated = queryset.update(status='WON')
        self.message_user(request, f"{updated} prospect(s) marked as won.")
    mark_as_won.short_description = "✓ Mark as Won"
    
    def mark_as_lost(self, request, queryset):
        updated = queryset.update(status='LOST')
        self.message_user(request, f"{updated} prospect(s) marked as lost.")
    mark_as_lost.short_description = "✗ Mark as Lost"


@admin.register(VisitLog)
class VisitLogAdmin(admin.ModelAdmin):
    list_display = ('visit_id', 'get_employee_info', 'get_prospect_info', 'visit_date', 
                   'visit_time', 'outcome_badge', 'status_badge', 'approval_badge')
    list_filter = ('status', 'approval_status', 'outcome_type', 'visit_date', 
                   'sales_employee__department', 'sales_employee__region', 'created_at')
    search_fields = ('visit_id', 'sales_employee__employee_id', 'sales_employee__user__username',
                    'prospect__name', 'prospect__company_name', 'meeting_agenda', 'meeting_outcome')
    readonly_fields = ('visit_id', 'created_at', 'updated_at', 'approved_at', 'approved_by')
    date_hierarchy = 'visit_date'
    list_per_page = 30
    
    fieldsets = (
        ('Visit Information', {
            'fields': ('visit_id', 'sales_employee', 'prospect', 'visit_date', 'visit_time'),
            'description': 'Basic visit identification and scheduling'
        }),
        ('Meeting Details', {
            'fields': ('meeting_agenda', 'meeting_outcome', 'outcome_type', 'next_follow_up_date'),
            'description': 'Meeting agenda, outcomes, and follow-up planning'
        }),
        ('Status & Approval', {
            'fields': ('status', 'approval_status', 'approved_by', 'approved_at'),
            'description': 'Visit status and approval workflow'
        }),
        ('Location', {
            'fields': ('location', 'gps_latitude', 'gps_longitude'),
            'classes': ('collapse',),
            'description': 'GPS tracking and location verification'
        }),
        ('Attachments', {
            'fields': ('visiting_card', 'photo', 'document'),
            'classes': ('collapse',),
            'description': 'Supporting documents and photos'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_employee_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small style="color: #666;">{}</small>',
            obj.sales_employee.user.get_full_name() or obj.sales_employee.user.username,
            obj.sales_employee.employee_id
        )
    get_employee_info.short_description = 'Employee'
    
    def get_prospect_info(self, obj):
        company = f" - {obj.prospect.company_name}" if obj.prospect.company_name else ""
        return format_html(
            '<strong>{}</strong><br><small style="color: #666;">{}{}</small>',
            obj.prospect.name,
            obj.prospect.city,
            company
        )
    get_prospect_info.short_description = 'Prospect'
    
    def outcome_badge(self, obj):
        if not obj.outcome_type:
            return '-'
        colors = {
            'POSITIVE': '#28a745',
            'NEUTRAL': '#6c757d',
            'NEGATIVE': '#dc3545',
            'DEAL_CLOSED': '#007bff',
            'FOLLOW_UP': '#ffc107',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.outcome_type, '#6c757d'),
            obj.get_outcome_type_display()
        )
    outcome_badge.short_description = 'Outcome'
    
    def status_badge(self, obj):
        colors = {
            'SCHEDULED': '#FFA500',
            'COMPLETED': '#28a745',
            'CANCELLED': '#dc3545'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def approval_badge(self, obj):
        colors = {
            'PENDING': '#FFA500',
            'APPROVED': '#28a745',
            'REJECTED': '#dc3545'
        }
        icon = {'PENDING': '⏳', 'APPROVED': '✓', 'REJECTED': '✗'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{} {}</span>',
            colors.get(obj.approval_status, '#6c757d'),
            icon.get(obj.approval_status, ''),
            obj.get_approval_status_display()
        )
    approval_badge.short_description = 'Approval'
    
    actions = ['approve_visits', 'reject_visits', 'mark_as_completed']
    
    def approve_visits(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(approval_status='PENDING').update(
            approval_status='APPROVED',
            approved_by=request.user,
            approved_at=timezone.now()
        )
        self.message_user(request, f"{updated} visit(s) approved successfully.")
    approve_visits.short_description = "✓ Approve selected visits"
    
    def reject_visits(self, request, queryset):
        from django.utils import timezone
        updated = queryset.filter(approval_status='PENDING').update(
            approval_status='REJECTED',
            approved_by=request.user,
            approved_at=timezone.now()
        )
        self.message_user(request, f"{updated} visit(s) rejected.")
    reject_visits.short_description = "✗ Reject selected visits"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f"{updated} visit(s) marked as completed.")
    mark_as_completed.short_description = "✓ Mark as Completed"


# ==========================
# LEAD MANAGEMENT
# ==========================

class LeadHistoryInline(admin.TabularInline):
    model = LeadHistory
    extra = 0
    readonly_fields = ('changed_by', 'field_name', 'old_value', 'new_value', 'notes', 'changed_at')
    can_delete = False
    max_num = 0  # Don't allow adding new history entries manually
    
    fields = ('changed_at', 'changed_by', 'field_name', 'old_value', 'new_value', 'notes')


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('lead_id', 'get_prospect_info', 'source_badge', 'assigned_to', 
                   'status_badge', 'priority_badge', 'progress_bar', 'expected_closure_date',
                   'next_action_date', 'estimated_value', 'created_at')
    list_filter = ('lead_source', 'status', 'priority', 'assigned_to__department', 
                  'expected_closure_date', 'next_action_date', 'created_at')
    search_fields = ('lead_id', 'prospect__name', 'prospect__company_name', 'contact_person',
                    'mobile', 'email', 'requirement_description')
    readonly_fields = ('lead_id', 'created_at', 'updated_at', 'created_by')
    date_hierarchy = 'created_at'
    list_per_page = 30
    inlines = [LeadHistoryInline]
    
    fieldsets = (
        ('Lead Information', {
            'fields': ('lead_id', 'lead_source', 'prospect', 'originating_visit'),
            'description': 'Basic lead identification and source tracking'
        }),
        ('Contact Details', {
            'fields': ('contact_person', 'mobile', 'email')
        }),
        ('Requirement', {
            'fields': ('requirement_description', 'estimated_value', 'priority'),
            'description': 'Customer requirements and deal value'
        }),
        ('Assignment & Status', {
            'fields': ('assigned_to', 'status', 'progress_percentage'),
            'description': 'Lead ownership and current status'
        }),
        ('Timeline', {
            'fields': ('expected_closure_date', 'next_action_date', 'next_action_notes'),
            'description': 'Key dates and action planning'
        }),
        ('Additional Information', {
            'fields': ('notes', 'lost_reason', 'actual_value'),
            'classes': ('collapse',)
        }),
        ('Audit', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_prospect_info(self, obj):
        company = f" - {obj.prospect.company_name}" if obj.prospect.company_name else ""
        return format_html(
            '<strong>{}</strong><br><small style="color: #666;">{}</small>',
            obj.prospect.name,
            company or obj.contact_person
        )
    get_prospect_info.short_description = 'Prospect'
    
    def source_badge(self, obj):
        colors = {
            'VISIT': '#007bff',
            'REFERENCE': '#17a2b8',
            'WEB': '#20c997',
            'CAMPAIGN': '#6f42c1',
            'COLD_CALL': '#fd7e14',
            'SOCIAL_MEDIA': '#e83e8c',
            'DIRECT': '#28a745',
            'OTHER': '#6c757d',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.lead_source, '#6c757d'),
            obj.get_lead_source_display()
        )
    source_badge.short_description = 'Source'
    
    def status_badge(self, obj):
        colors = {
            'NEW': '#007bff',
            'CONTACTED': '#17a2b8',
            'QUALIFIED': '#20c997',
            'PROPOSAL_SENT': '#6f42c1',
            'IN_NEGOTIATION': '#fd7e14',
            'WON': '#28a745',
            'LOST': '#dc3545',
            'HOLD': '#ffc107',
            'CLOSED': '#6c757d',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px; font-weight: bold;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def priority_badge(self, obj):
        colors = {
            'LOW': '#6c757d',
            'MEDIUM': '#17a2b8',
            'HIGH': '#fd7e14',
            'URGENT': '#dc3545',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.priority, '#6c757d'),
            obj.priority.title()
        )
    priority_badge.short_description = 'Priority'
    
    def progress_bar(self, obj):
        color = '#28a745' if obj.progress_percentage >= 75 else '#ffc107' if obj.progress_percentage >= 50 else '#fd7e14' if obj.progress_percentage >= 25 else '#dc3545'
        return format_html(
            '<div style="width: 100px; background: #e9ecef; border-radius: 3px; overflow: hidden;">'
            '<div style="width: {}%; background: {}; color: white; text-align: center; padding: 2px 0; font-size: 10px; font-weight: bold;">{}</div>'
            '</div>',
            obj.progress_percentage,
            color,
            f'{obj.progress_percentage}%'
        )
    progress_bar.short_description = 'Progress'
    
    actions = ['mark_as_won', 'mark_as_lost', 'mark_as_contacted', 'assign_to_employee']
    
    def mark_as_won(self, request, queryset):
        updated = queryset.update(status='WON', progress_percentage=100)
        self.message_user(request, f"{updated} lead(s) marked as won.")
    mark_as_won.short_description = "✓ Mark as Won"
    
    def mark_as_lost(self, request, queryset):
        updated = queryset.update(status='LOST')
        self.message_user(request, f"{updated} lead(s) marked as lost.")
    mark_as_lost.short_description = "✗ Mark as Lost"
    
    def mark_as_contacted(self, request, queryset):
        updated = queryset.filter(status='NEW').update(status='CONTACTED', progress_percentage=10)
        self.message_user(request, f"{updated} lead(s) marked as contacted.")
    mark_as_contacted.short_description = "📞 Mark as Contacted"


@admin.register(LeadHistory)
class LeadHistoryAdmin(admin.ModelAdmin):
    list_display = ('lead', 'field_name', 'old_value_short', 'new_value_short', 'changed_by', 'changed_at')
    list_filter = ('field_name', 'changed_at', 'changed_by')
    search_fields = ('lead__lead_id', 'lead__prospect__name', 'field_name', 'old_value', 'new_value', 'notes')
    readonly_fields = ('lead', 'changed_by', 'field_name', 'old_value', 'new_value', 'notes', 'changed_at')
    date_hierarchy = 'changed_at'
    
    def has_add_permission(self, request):
        return False  # Prevent manual creation
    
    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletion
    
    def old_value_short(self, obj):
        if obj.old_value and len(obj.old_value) > 50:
            return obj.old_value[:50] + '...'
        return obj.old_value or '-'
    old_value_short.short_description = 'Old Value'
    
    def new_value_short(self, obj):
        if obj.new_value and len(obj.new_value) > 50:
            return obj.new_value[:50] + '...'
        return obj.new_value or '-'
    new_value_short.short_description = 'New Value'


# ==========================
# ACTIVITY TRACKER
# ==========================

@admin.register(LeadActivity)
class LeadActivityAdmin(admin.ModelAdmin):
    list_display = ('activity_id', 'get_lead_info', 'activity_type_badge', 'activity_date', 
                   'activity_time', 'status_badge', 'next_followup_date', 'created_by', 'created_at')
    list_filter = ('activity_type', 'status', 'activity_date', 'lead__status', 
                   'lead__assigned_to', 'created_at')
    search_fields = ('activity_id', 'lead__lead_id', 'lead__prospect__name', 
                    'discussion_summary', 'outcome', 'contact_person')
    readonly_fields = ('activity_id', 'created_at', 'updated_at', 'created_by')
    date_hierarchy = 'activity_date'
    list_per_page = 30
    
    fieldsets = (
        ('Activity Information', {
            'fields': ('activity_id', 'lead', 'activity_type', 'activity_date', 'activity_time'),
            'description': 'Basic activity identification and scheduling'
        }),
        ('Discussion Details', {
            'fields': ('discussion_summary', 'outcome', 'remarks'),
            'description': 'Summary of the interaction and outcomes'
        }),
        ('Follow-up Planning', {
            'fields': ('next_followup_date', 'next_followup_time', 'next_action_required'),
            'description': 'Schedule and plan next actions'
        }),
        ('Status & Updates', {
            'fields': ('status', 'lead_status_update'),
            'description': 'Activity and lead status tracking'
        }),
        ('Contact Information', {
            'fields': ('contact_person', 'contact_number', 'contact_email'),
            'classes': ('collapse',)
        }),
        ('Attachments', {
            'fields': ('attachment1', 'attachment2', 'attachment3'),
            'classes': ('collapse',),
            'description': 'Upload proposals, emails, or other documents'
        }),
        ('Audit', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_lead_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small style="color: #666;">{}</small>',
            obj.lead.lead_id,
            obj.lead.prospect.name
        )
    get_lead_info.short_description = 'Lead'
    
    def activity_type_badge(self, obj):
        colors = {
            'CALL': '#007bff',
            'EMAIL': '#17a2b8',
            'MEETING': '#6f42c1',
            'WHATSAPP': '#25D366',
            'VISIT': '#fd7e14',
            'PROPOSAL': '#20c997',
            'DEMO': '#6610f2',
            'NEGOTIATION': '#e83e8c',
            'FOLLOWUP': '#ffc107',
            'OTHER': '#6c757d',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.activity_type, '#6c757d'),
            obj.get_activity_type_display()
        )
    activity_type_badge.short_description = 'Type'
    
    def status_badge(self, obj):
        colors = {
            'SCHEDULED': '#ffc107',
            'COMPLETED': '#28a745',
            'CANCELLED': '#dc3545',
            'RESCHEDULED': '#17a2b8',
        }
        icon = {'SCHEDULED': '📅', 'COMPLETED': '✓', 'CANCELLED': '✗', 'RESCHEDULED': '🔄'}
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{} {}</span>',
            colors.get(obj.status, '#6c757d'),
            icon.get(obj.status, ''),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    actions = ['mark_as_completed', 'mark_as_scheduled', 'mark_as_cancelled']
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='COMPLETED')
        self.message_user(request, f"{updated} activity(ies) marked as completed.")
    mark_as_completed.short_description = "✓ Mark as Completed"
    
    def mark_as_scheduled(self, request, queryset):
        updated = queryset.update(status='SCHEDULED')
        self.message_user(request, f"{updated} activity(ies) marked as scheduled.")
    mark_as_scheduled.short_description = "📅 Mark as Scheduled"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='CANCELLED')
        self.message_user(request, f"{updated} activity(ies) cancelled.")
    mark_as_cancelled.short_description = "✗ Cancel Activities"


# ==========================
# QUOTATION MANAGEMENT
# ==========================

class QuotationItemInline(admin.TabularInline):
    model = QuotationItem
    extra = 1
    fields = ('line_number', 'item_code', 'description', 'quantity', 'uom', 'unit_price', 
              'discount_percentage', 'tax_percentage', 'line_total')
    readonly_fields = ('line_total',)


class QuotationAttachmentInline(admin.TabularInline):
    model = QuotationAttachment
    extra = 0
    fields = ('attachment_type', 'file', 'description', 'uploaded_by', 'uploaded_at')
    readonly_fields = ('uploaded_by', 'uploaded_at')


class QuotationActivityInline(admin.TabularInline):
    model = QuotationActivity
    extra = 0
    fields = ('activity_type', 'description', 'is_internal', 'created_by', 'created_at')
    readonly_fields = ('created_by', 'created_at')


@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):
    list_display = ('quote_number', 'get_prospect_info', 'quote_date', 'valid_till_badge', 
                   'net_amount_display', 'status_badge', 'assigned_to_display', 'created_at')
    list_filter = ('status', 'currency', 'quote_date', 'valid_till', 'assigned_to', 'created_at')
    search_fields = ('quote_number', 'prospect__name', 'prospect__company_name', 
                    'contact_person', 'reference_number')
    readonly_fields = ('quote_number', 'created_by', 'created_at', 'updated_at', 
                      'approved_by', 'approved_at', 'sent_at')
    date_hierarchy = 'quote_date'
    list_per_page = 25
    
    fieldsets = (
        ('Quote Information', {
            'fields': ('quote_number', 'quote_date', 'valid_till', 'status'),
        }),
        ('Customer Details', {
            'fields': ('prospect', 'contact_person', 'contact_email', 'contact_phone'),
        }),
        ('Assignment & Reference', {
            'fields': ('assigned_to', 'reference_lead', 'reference_visit', 'reference_number'),
        }),
        ('Currency & Amounts', {
            'fields': ('currency', 'exchange_rate', 'subtotal', 'discount_percentage', 
                      'discount_amount', 'tax_amount', 'freight_charges', 'net_amount'),
        }),
        ('Terms & Conditions', {
            'fields': ('payment_terms', 'delivery_terms'),
            'classes': ('collapse',)
        }),
        ('Remarks', {
            'fields': ('customer_remarks', 'internal_notes'),
            'classes': ('collapse',)
        }),
        ('Approval & Workflow', {
            'fields': ('approved_by', 'approved_at', 'sent_at', 'converted_to_order', 
                      'order_number', 'order_date'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [QuotationItemInline, QuotationAttachmentInline, QuotationActivityInline]
    
    def get_prospect_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small style="color: #666;">{}</small>',
            obj.prospect.name,
            obj.prospect.company_name or 'N/A'
        )
    get_prospect_info.short_description = 'Customer'
    
    def valid_till_badge(self, obj):
        if obj.is_expired:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">⚠️ Expired</span>'
            )
        elif obj.days_to_expire <= 3:
            return format_html(
                '<span style="background-color: #ffc107; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">⏰ {} days</span>',
                obj.days_to_expire
            )
        else:
            return format_html(
                '<span style="color: #28a745;">✓ Valid</span>'
            )
    valid_till_badge.short_description = 'Validity'
    
    def net_amount_display(self, obj):
        return format_html(
            '<strong>{} {:,.2f}</strong>',
            obj.currency,
            obj.net_amount
        )
    net_amount_display.short_description = 'Net Amount'
    
    def status_badge(self, obj):
        colors = {
            'DRAFT': '#6c757d',
            'PENDING': '#ffc107',
            'APPROVED': '#28a745',
            'SENT': '#17a2b8',
            'ACCEPTED': '#28a745',
            'REJECTED': '#dc3545',
            'REVISED': '#fd7e14',
            'CONVERTED': '#6f42c1',
            'EXPIRED': '#dc3545',
            'CANCELLED': '#6c757d',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def assigned_to_display(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.user.get_full_name() or obj.assigned_to.user.username
        return '-'
    assigned_to_display.short_description = 'Assigned To'
    
    actions = ['mark_as_sent', 'mark_as_approved', 'mark_as_rejected']
    
    def mark_as_sent(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='SENT', sent_at=timezone.now())
        self.message_user(request, f"{updated} quotation(s) marked as sent.")
    mark_as_sent.short_description = "📤 Mark as Sent"
    
    def mark_as_approved(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='APPROVED', approved_by=request.user, approved_at=timezone.now())
        self.message_user(request, f"{updated} quotation(s) approved.")
    mark_as_approved.short_description = "✅ Approve Quotations"
    
    def mark_as_rejected(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f"{updated} quotation(s) rejected.")
    mark_as_rejected.short_description = "❌ Reject Quotations"


@admin.register(QuotationItem)
class QuotationItemAdmin(admin.ModelAdmin):
    list_display = ('quotation', 'line_number', 'item_code', 'description_short', 
                   'quantity', 'uom', 'unit_price', 'line_total')
    list_filter = ('quotation__status', 'uom')
    search_fields = ('quotation__quote_number', 'item_code', 'description')
    list_per_page = 50
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'


@admin.register(QuotationAttachment)
class QuotationAttachmentAdmin(admin.ModelAdmin):
    list_display = ('quotation', 'attachment_type', 'file_name', 'uploaded_by', 'uploaded_at')
    list_filter = ('attachment_type', 'uploaded_at')
    search_fields = ('quotation__quote_number', 'file_name', 'description')
    readonly_fields = ('uploaded_by', 'uploaded_at')
    list_per_page = 30


@admin.register(QuotationActivity)
class QuotationActivityAdmin(admin.ModelAdmin):
    list_display = ('quotation', 'activity_type', 'description_short', 'is_internal', 
                   'created_by', 'created_at')
    list_filter = ('activity_type', 'is_internal', 'created_at')
    search_fields = ('quotation__quote_number', 'description')
    readonly_fields = ('created_by', 'created_at')
    list_per_page = 50
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'


# ==========================
# SALES ORDER ADMINISTRATION
# ==========================

class SalesOrderItemInline(admin.TabularInline):
    model = SalesOrderItem
    extra = 1
    fields = ('line_number', 'item_code', 'description', 'quantity', 'uom', 'unit_price', 
              'discount_percentage', 'tax_percentage', 'line_total')
    readonly_fields = ('line_total',)


class SalesOrderAttachmentInline(admin.TabularInline):
    model = SalesOrderAttachment
    extra = 0
    fields = ('attachment_type', 'file', 'description', 'uploaded_by', 'uploaded_at')
    readonly_fields = ('uploaded_by', 'uploaded_at')


class SalesOrderActivityInline(admin.TabularInline):
    model = SalesOrderActivity
    extra = 0
    fields = ('activity_type', 'description', 'is_internal', 'created_by', 'created_at')
    readonly_fields = ('created_by', 'created_at')


@admin.register(SalesOrder)
class SalesOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'get_prospect_info', 'order_date', 'valid_till_badge', 
                   'net_amount_display', 'status_badge', 'assigned_to_display', 'created_at')
    list_filter = ('status', 'currency', 'order_date', 'valid_till', 'assigned_to', 'created_at')
    search_fields = ('order_number', 'prospect__name', 'prospect__company_name', 
                    'contact_person', 'reference_number')
    readonly_fields = ('order_number', 'created_by', 'created_at', 'updated_at', 
                      'approved_by', 'approved_at', 'confirmed_at', 'shipped_at', 'delivered_at')
    date_hierarchy = 'order_date'
    list_per_page = 25
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'order_date', 'valid_till', 'status'),
        }),
        ('Customer Details', {
            'fields': ('prospect', 'contact_person', 'contact_email', 'contact_phone'),
        }),
        ('Assignment & Reference', {
            'fields': ('assigned_to', 'reference_lead', 'reference_visit', 'reference_quotation', 'reference_number'),
        }),
        ('Currency & Amounts', {
            'fields': ('currency', 'exchange_rate', 'subtotal', 'discount_percentage', 
                      'discount_amount', 'tax_amount', 'freight_charges', 'net_amount'),
        }),
        ('Terms & Conditions', {
            'fields': ('payment_terms', 'delivery_terms'),
            'classes': ('collapse',)
        }),
        ('Remarks', {
            'fields': ('customer_remarks', 'internal_notes'),
            'classes': ('collapse',)
        }),
        ('Order Lifecycle', {
            'fields': ('approved_by', 'approved_at', 'confirmed_at', 'shipped_at', 'delivered_at'),
            'classes': ('collapse',)
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [SalesOrderItemInline, SalesOrderAttachmentInline, SalesOrderActivityInline]
    
    def get_prospect_info(self, obj):
        return format_html(
            '<strong>{}</strong><br><small style="color: #666;">{}</small>',
            obj.prospect.name,
            obj.prospect.company_name or 'N/A'
        )
    get_prospect_info.short_description = 'Customer'
    
    def valid_till_badge(self, obj):
        if obj.is_expired:
            return format_html(
                '<span style="background-color: #dc3545; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">⚠️ Expired</span>'
            )
        elif obj.days_to_expire <= 3:
            return format_html(
                '<span style="background-color: #ffc107; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">⏰ {} days</span>',
                obj.days_to_expire
            )
        else:
            return format_html(
                '<span style="color: #28a745;">✓ Valid</span>'
            )
    valid_till_badge.short_description = 'Validity'
    
    def net_amount_display(self, obj):
        return format_html(
            '<strong>{} {:,.2f}</strong>',
            obj.currency,
            obj.net_amount
        )
    net_amount_display.short_description = 'Net Amount'
    
    def status_badge(self, obj):
        colors = {
            'DRAFT': '#6c757d',
            'PENDING': '#ffc107',
            'APPROVED': '#28a745',
            'CONFIRMED': '#17a2b8',
            'PROCESSING': '#fd7e14',
            'SHIPPED': '#6f42c1',
            'DELIVERED': '#28a745',
            'COMPLETED': '#28a745',
            'CANCELLED': '#dc3545',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 3px; font-size: 11px;">{}</span>',
            colors.get(obj.status, '#6c757d'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status'
    
    def assigned_to_display(self, obj):
        if obj.assigned_to:
            return obj.assigned_to.user.get_full_name() or obj.assigned_to.user.username
        return '-'
    assigned_to_display.short_description = 'Assigned To'
    
    actions = ['mark_as_confirmed', 'mark_as_approved', 'mark_as_cancelled']
    
    def mark_as_confirmed(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='CONFIRMED', confirmed_at=timezone.now())
        self.message_user(request, f"{updated} order(s) marked as confirmed.")
    mark_as_confirmed.short_description = "✓ Mark as Confirmed"
    
    def mark_as_approved(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(status='APPROVED', approved_by=request.user, approved_at=timezone.now())
        self.message_user(request, f"{updated} order(s) approved.")
    mark_as_approved.short_description = "✅ Approve Orders"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='CANCELLED')
        self.message_user(request, f"{updated} order(s) cancelled.")
    mark_as_cancelled.short_description = "❌ Cancel Orders"


@admin.register(SalesOrderItem)
class SalesOrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'line_number', 'item_code', 'description_short', 
                   'quantity', 'uom', 'unit_price', 'line_total')
    list_filter = ('order__status', 'uom')
    search_fields = ('order__order_number', 'item_code', 'description')
    list_per_page = 50
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'


@admin.register(SalesOrderAttachment)
class SalesOrderAttachmentAdmin(admin.ModelAdmin):
    list_display = ('order', 'attachment_type', 'file_name', 'uploaded_by', 'uploaded_at')
    list_filter = ('attachment_type', 'uploaded_at')
    search_fields = ('order__order_number', 'file_name', 'description')
    readonly_fields = ('uploaded_by', 'uploaded_at')
    list_per_page = 30


@admin.register(SalesOrderActivity)
class SalesOrderActivityAdmin(admin.ModelAdmin):
    list_display = ('order', 'activity_type', 'description_short', 'is_internal', 
                   'created_by', 'created_at')
    list_filter = ('activity_type', 'is_internal', 'created_at')
    search_fields = ('order__order_number', 'description')
    readonly_fields = ('created_by', 'created_at')
    list_per_page = 50
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'


# =====================================================
# MASTER DATA MANAGEMENT ADMIN
# =====================================================

@admin.register(ItemMaster)
class ItemMasterAdmin(admin.ModelAdmin):
    list_display = ('item_code', 'description_short', 'item_type', 'unit_of_measurement', 
                   'standard_price', 'default_tax_percentage', 'is_active_badge', 'created_at')
    list_filter = ('item_type', 'is_active', 'category', 'brand', 'created_at')
    search_fields = ('item_code', 'description', 'short_name', 'hsn_sac_code', 'manufacturer', 'brand')
    readonly_fields = ('created_by', 'created_at', 'updated_at')
    list_per_page = 50
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('item_code', 'description', 'short_name', 'item_type', 'unit_of_measurement')
        }),
        ('Pricing', {
            'fields': ('standard_price', 'minimum_price', 'purchase_price')
        }),
        ('Tax & Compliance', {
            'fields': ('hsn_sac_code', 'default_tax_percentage')
        }),
        ('Classification', {
            'fields': ('category', 'manufacturer', 'brand')
        }),
        ('Status & Remarks', {
            'fields': ('is_active', 'remarks')
        }),
        ('Tracking', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def description_short(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_short.short_description = 'Description'
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ Active</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(TaxMaster)
class TaxMasterAdmin(admin.ModelAdmin):
    list_display = ('tax_code', 'tax_name', 'tax_type', 'tax_percentage', 'hsn_sac_code', 
                   'is_active_badge', 'created_at')
    list_filter = ('tax_type', 'is_active', 'created_at')
    search_fields = ('tax_code', 'tax_name', 'hsn_sac_code')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 50
    
    fieldsets = (
        ('Tax Details', {
            'fields': ('tax_code', 'tax_name', 'tax_type', 'tax_percentage')
        }),
        ('Compliance', {
            'fields': ('hsn_sac_code', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ Active</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'


@admin.register(PaymentTermsMaster)
class PaymentTermsMasterAdmin(admin.ModelAdmin):
    list_display = ('term_code', 'term_name', 'days', 'is_active_badge', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('term_code', 'term_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 50
    
    fieldsets = (
        ('Payment Terms', {
            'fields': ('term_code', 'term_name', 'days', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ Active</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'


@admin.register(DeliveryTermsMaster)
class DeliveryTermsMasterAdmin(admin.ModelAdmin):
    list_display = ('term_code', 'term_name', 'inco_term', 'is_active_badge', 'created_at')
    list_filter = ('inco_term', 'is_active', 'created_at')
    search_fields = ('term_code', 'term_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 50
    
    fieldsets = (
        ('Delivery Terms', {
            'fields': ('term_code', 'term_name', 'inco_term', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ Active</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'


@admin.register(VisitPurposeMaster)
class VisitPurposeMasterAdmin(admin.ModelAdmin):
    list_display = ('purpose_code', 'purpose_name', 'is_active_badge', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('purpose_code', 'purpose_name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 50
    
    fieldsets = (
        ('Visit Purpose', {
            'fields': ('purpose_code', 'purpose_name', 'description')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ Active</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'


@admin.register(ApprovalMatrix)
class ApprovalMatrixAdmin(admin.ModelAdmin):
    list_display = ('document_type', 'min_amount', 'max_amount', 'approver_role', 
                   'approver', 'is_active_badge', 'created_at')
    list_filter = ('document_type', 'is_active', 'created_at')
    search_fields = ('approver_role', 'remarks')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 50
    
    fieldsets = (
        ('Approval Configuration', {
            'fields': ('document_type', 'min_amount', 'max_amount')
        }),
        ('Approver Details', {
            'fields': ('approver_role', 'approver')
        }),
        ('Additional Info', {
            'fields': ('remarks', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_active_badge(self, obj):
        if obj.is_active:
            return format_html('<span style="color: green; font-weight: bold;">✓ Active</span>')
        return format_html('<span style="color: red; font-weight: bold;">✗ Inactive</span>')
    is_active_badge.short_description = 'Status'


# =====================================================
# SERVICE CALL MANAGEMENT ADMIN
# =====================================================

@admin.register(Technician)
class TechnicianAdmin(admin.ModelAdmin):
    """Comprehensive admin panel for Technician Master"""
    list_display = ('employee_code', 'full_name_display', 'mobile', 'email', 'skill_level', 
                   'region', 'active_calls', 'is_active', 'is_available', 'joining_date')
    list_filter = ('skill_level', 'is_active', 'is_available', 'region', 'territory', 
                  'department', 'joining_date', 'created_at')
    search_fields = ('employee_code', 'user__first_name', 'user__last_name', 'user__username',
                    'mobile', 'alternate_mobile', 'email', 'alternate_email', 'specialization',
                    'city', 'state', 'aadhar_number', 'pan_number')
    readonly_fields = ('employee_code', 'created_at', 'updated_at', 'active_calls_count_display')
    list_editable = ('is_active', 'is_available')
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee_code', 'user', 'joining_date', 'department', 'designation', 'reporting_to')
        }),
        ('Contact Details', {
            'fields': ('mobile', 'alternate_mobile', 'email', 'alternate_email', 
                      'address', 'city', 'state', 'pincode')
        }),
        ('Professional Details', {
            'fields': ('skill_level', 'specialization', 'region', 'territory')
        }),
        ('Personal Information', {
            'fields': ('emergency_contact_name', 'emergency_contact_phone', 
                      'aadhar_number', 'pan_number', 'license_number'),
            'classes': ('collapse',)
        }),
        ('Status & Availability', {
            'fields': ('is_active', 'is_available', 'active_calls_count_display')
        }),
        ('Additional Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def full_name_display(self, obj):
        """Display full name with styling"""
        name = obj.user.get_full_name() or obj.user.username
        if not obj.is_active:
            return format_html('<span style="color: #999; text-decoration: line-through;">{}</span>', name)
        return name
    full_name_display.short_description = 'Name'
    full_name_display.admin_order_field = 'user__first_name'
    
    def active_calls(self, obj):
        """Display count of active service calls"""
        count = obj.active_service_calls_count
        if count > 0:
            return format_html(
                '<span style="background-color: #ffc107; color: black; padding: 2px 8px; border-radius: 3px; font-weight: bold;">{}</span>',
                count
            )
        return format_html('<span style="color: #28a745;">0</span>', count)
    active_calls.short_description = 'Active Calls'
    active_calls.admin_order_field = 'assigned_calls'
    
    def active_calls_count_display(self, obj):
        """Read-only field showing active service calls count"""
        count = obj.active_service_calls_count
        if count > 0:
            return format_html(
                '<strong style="color: #ffc107;">{} active service call(s)</strong>',
                count
            )
        return "No active service calls"
    active_calls_count_display.short_description = 'Active Service Calls'
    
    actions = ['activate_technicians', 'deactivate_technicians', 'make_available', 'make_unavailable']
    
    def activate_technicians(self, request, queryset):
        """Bulk activate technicians"""
        updated = queryset.update(is_active=True)
        self.message_user(request, f"{updated} technician(s) activated successfully.")
    activate_technicians.short_description = "Activate selected technicians"
    
    def deactivate_technicians(self, request, queryset):
        """Bulk deactivate technicians"""
        updated = queryset.update(is_active=False)
        self.message_user(request, f"{updated} technician(s) deactivated successfully.")
    deactivate_technicians.short_description = "Deactivate selected technicians"
    
    def make_available(self, request, queryset):
        """Mark technicians as available"""
        updated = queryset.update(is_available=True)
        self.message_user(request, f"{updated} technician(s) marked as available.")
    make_available.short_description = "Mark as available"
    
    def make_unavailable(self, request, queryset):
        """Mark technicians as unavailable"""
        updated = queryset.update(is_available=False)
        self.message_user(request, f"{updated} technician(s) marked as unavailable.")
    make_unavailable.short_description = "Mark as unavailable"
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        qs = super().get_queryset(request)
        return qs.select_related('user', 'territory', 'department', 'designation', 'reporting_to')


@admin.register(ServiceContract)
class ServiceContractAdmin(admin.ModelAdmin):
    list_display = ('contract_number', 'customer', 'contract_type', 'start_date', 'end_date', 'status')
    list_filter = ('contract_type', 'status', 'start_date')
    search_fields = ('contract_number', 'customer__name')
    readonly_fields = ('contract_number',)
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(WarrantyRecord)
class WarrantyRecordAdmin(admin.ModelAdmin):
    list_display = ('warranty_number', 'customer', 'product_description', 'warranty_type', 'start_date', 'end_date', 'status')
    list_filter = ('warranty_type', 'status')
    search_fields = ('warranty_number', 'customer__name', 'product_serial_number')


class ServiceCallItemInline(admin.TabularInline):
    model = ServiceCallItem
    extra = 1
    fields = ('line_number', 'item_type', 'item_code', 'product_serial_no', 'description', 'fault_found',
             'quantity', 'unit_cost', 'unit_price', 'labour_hours', 'labour_rate', 
             'warranty_covered', 'batch_no', 'line_total')
    readonly_fields = ('line_total',)


class ServiceActivityInline(admin.TabularInline):
    model = ServiceActivity
    extra = 1
    fields = ('activity_type', 'activity_date', 'performed_by', 'duration_minutes')


@admin.register(ServiceCall)
class ServiceCallAdmin(admin.ModelAdmin):
    list_display = ('service_number', 'customer', 'service_type', 'priority', 'status', 
                   'assigned_technician', 'service_request_date', 'billable', 'actual_cost')
    list_filter = ('service_type', 'priority', 'status', 'billable', 'warranty_status')
    search_fields = ('service_number', 'customer__name', 'contact_person', 'problem_description')
    readonly_fields = ('service_number',)
    
    inlines = [ServiceCallItemInline, ServiceActivityInline]
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        obj.updated_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ServiceCallItem)
class ServiceCallItemAdmin(admin.ModelAdmin):
    list_display = ('service_call', 'line_number', 'item_type', 'item_code', 'product_serial_no', 
                   'quantity', 'unit_price', 'labour_hours', 'warranty_covered', 'line_total')
    list_filter = ('item_type', 'warranty_covered')
    search_fields = ('service_call__service_number', 'item_code', 'product_serial_no', 
                    'description', 'batch_no', 'serial_number')
    readonly_fields = ('line_total',)
    
    fieldsets = (
        ('Service Call', {
            'fields': ('service_call', 'line_number')
        }),
        ('Item Details', {
            'fields': ('item_master', 'item_type', 'item_code', 'product_serial_no', 'description', 'fault_found')
        }),
        ('Quantity & Pricing', {
            'fields': ('quantity', 'uom', 'unit_cost', 'unit_price')
        }),
        ('Labour Charges', {
            'fields': ('labour_hours', 'labour_rate')
        }),
        ('Tax & Total', {
            'fields': ('tax_percentage', 'line_total')
        }),
        ('Warranty & Traceability', {
            'fields': ('warranty_covered', 'batch_no', 'serial_number')
        }),
        ('Additional Info', {
            'fields': ('remarks',)
        }),
    )


@admin.register(ServiceActivity)
class ServiceActivityAdmin(admin.ModelAdmin):
    list_display = ('service_call', 'activity_type', 'activity_date', 'performed_by', 'duration_minutes', 'is_billable')
    list_filter = ('activity_type', 'is_billable', 'activity_date')
    search_fields = ('service_call__service_number', 'description')


@admin.register(ServiceCallAttachment)
class ServiceCallAttachmentAdmin(admin.ModelAdmin):
    list_display = ('service_call', 'file_name', 'file_type', 'uploaded_by', 'uploaded_at')
    list_filter = ('file_type', 'uploaded_at')
    search_fields = ('service_call__service_number', 'file_name')


# =====================================================
# SPARE PARTS USAGE & INVOICING
# =====================================================

@admin.register(SpareUsage)
class SpareUsageAdmin(admin.ModelAdmin):
    list_display = ('service_call', 'part', 'qty_used', 'cost_price', 'sell_price', 'warehouse_id', 'replacement_reason', 'verified_at')
    list_filter = ('replacement_reason', 'verified_at')
    search_fields = ('service_call__service_number', 'part__item_code', 'part__description')
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'


@admin.register(ServiceInvoice)
class ServiceInvoiceAdmin(admin.ModelAdmin):
    list_display = ('service_invoice_id', 'service_call', 'invoice_date', 'total_amount', 'payment_status', 'due_date')
    list_filter = ('payment_status', 'invoice_date', 'due_date')
    search_fields = ('service_invoice_id', 'service_call__service_number', 'invoice_number')
    readonly_fields = ('service_invoice_id', 'invoice_number',)
    date_hierarchy = 'invoice_date'


# =====================================================
# ADDITIONAL SERVICE MASTER DATA
# =====================================================

@admin.register(FaultCategory)
class FaultCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_code', 'category_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('category_code', 'category_name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SymptomMaster)
class SymptomMasterAdmin(admin.ModelAdmin):
    list_display = ('symptom_code', 'symptom_name', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('symptom_code', 'symptom_name', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SLAConfig)
class SLAConfigAdmin(admin.ModelAdmin):
    list_display = ('service_type', 'priority', 'response_time_sla_hours', 'resolution_time_sla_hours', 'is_active')
    list_filter = ('service_type', 'priority', 'is_active')
    search_fields = ('service_type', 'priority')
    readonly_fields = ('created_at', 'updated_at')
