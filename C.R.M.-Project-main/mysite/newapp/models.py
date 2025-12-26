from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class Department(models.Model):
    """Department master for organizational structure"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.code})"
    
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"
        ordering = ['name']


class Designation(models.Model):
    """Designation master for job roles"""
    title = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='designations')
    level = models.IntegerField(default=1, help_text="Hierarchy level (1=Top, higher=Lower)")
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.title} ({self.code})"
    
    class Meta:
        verbose_name = "Designation"
        verbose_name_plural = "Designations"
        ordering = ['level', 'title']


class Territory(models.Model):
    """Territory/Zone master for geographical mapping"""
    ZONE_TYPES = [
        ('ZONE', 'Zone'),
        ('REGION', 'Region'),
        ('STATE', 'State'),
        ('DISTRICT', 'District'),
        ('CITY', 'City'),
    ]
    
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    zone_type = models.CharField(max_length=20, choices=ZONE_TYPES, default='REGION')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='sub_territories')
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.zone_type})"
    
    class Meta:
        verbose_name = "Territory"
        verbose_name_plural = "Territories"
        ordering = ['zone_type', 'name']

class UserProfile(models.Model):
    """Extended user profile model for additional user information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(max_length=500, blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Automatically create a UserProfile when a new User is created"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the UserProfile when the User is saved"""
    if hasattr(instance, 'profile'):
        instance.profile.save()


class SalesEmployee(models.Model):
    """Sales employee model linked to User for CRM functionality"""
    ROLE_CHOICES = [
        ('SALES_REP', 'Sales Representative'),
        ('SALES_EXECUTIVE', 'Sales Executive'),
        ('SALES_HEAD', 'Sales Head'),
        ('MANAGER', 'Manager'),
        ('ADMIN', 'Admin'),
    ]
    
    REGION_CHOICES = [
        ('NORTH', 'North'),
        ('SOUTH', 'South'),
        ('EAST', 'East'),
        ('WEST', 'West'),
        ('CENTRAL', 'Central'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='sales_profile')
    employee_id = models.CharField(max_length=20, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='SALES_REP')
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    territory = models.ForeignKey(Territory, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, blank=True, null=True)
    reporting_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinates')
    mobile = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    joined_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.employee_id})"
    
    class Meta:
        verbose_name = "Sales Employee"
        verbose_name_plural = "Sales Employees"
        ordering = ['-created_at']


from django.db import models
from django.contrib.auth.models import User

class ProspectCustomer(models.Model):
    """Prospect/Customer master for CRM"""

    TYPE_CHOICES = [
        ('PROSPECT', 'Prospect'),
        ('CUSTOMER', 'Customer'),
        ('LEAD', 'Lead'),
    ]

    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('CONTACTED', 'Contacted'),
        ('QUALIFIED', 'Qualified'),
        ('PROPOSAL', 'Proposal Sent'),
        ('NEGOTIATION', 'In Negotiation'),
        ('WON', 'Won'),
        ('LOST', 'Lost'),
        ('INACTIVE', 'Inactive'),
    ]

    customer_id = models.CharField(
        max_length=50,
        unique=True,
        editable=False,
        db_index=True,
        null=True,
        blank=True
    )

    name = models.CharField(max_length=200, unique=True)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='PROSPECT')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, blank=True, null=True)

    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    industry = models.CharField(max_length=100, blank=True, null=True)

    assigned_to = models.ForeignKey(
        SalesEmployee,
        on_delete=models.SET_NULL,
        null=True,
        related_name='prospects'
    )

    notes = models.TextField(blank=True, null=True)

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_prospects'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    closed_at = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        """Auto-generate customer ID if not exists"""
        if not self.customer_id:
            last_customer = ProspectCustomer.objects.order_by('-id').first()

            if last_customer and last_customer.customer_id:
                try:
                    last_id = int(last_customer.customer_id.split('-')[-1])
                    self.customer_id = f"CUST-{last_id + 1:05d}"
                except (ValueError, IndexError):
                    self.customer_id = "CUST-00001"
            else:
                self.customer_id = "CUST-00001"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer_id} - {self.name} ({self.company_name or 'Individual'})"

    class Meta:
        verbose_name = "Prospect/Customer"
        verbose_name_plural = "Prospects/Customers"
        ordering = ['-created_at']

class Lead(models.Model):
    """Lead management model for tracking business opportunities"""
    SOURCE_CHOICES = [
        ('VISIT', 'Visit'),
        ('REFERENCE', 'Reference'),
        ('WEB', 'Website'),
        ('CAMPAIGN', 'Campaign'),
        ('COLD_CALL', 'Cold Call'),
        ('SOCIAL_MEDIA', 'Social Media'),
        ('DIRECT', 'Direct'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('NEW', 'New'),
        ('CONTACTED', 'Contacted'),
        ('QUALIFIED', 'Qualified'),
        ('PROPOSAL_SENT', 'Proposal Sent'),
        ('IN_NEGOTIATION', 'In Negotiation'),
        ('WON', 'Won'),
        ('LOST', 'Lost'),
        ('HOLD', 'Hold'),
        ('CLOSED', 'Closed'),
    ]
    
    lead_id = models.CharField(max_length=50, unique=True, editable=False)
    lead_source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    prospect = models.ForeignKey(ProspectCustomer, on_delete=models.CASCADE, related_name='leads')
    contact_person = models.CharField(max_length=200, help_text="Primary contact person name")
    mobile = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    requirement_description = models.TextField(help_text="Description of lead requirement")
    assigned_to = models.ForeignKey(SalesEmployee, on_delete=models.SET_NULL, null=True, related_name='assigned_leads')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    progress_percentage = models.IntegerField(default=0, help_text="Progress from 0-100%")
    expected_closure_date = models.DateField(blank=True, null=True)
    next_action_date = models.DateField(blank=True, null=True)
    next_action_notes = models.TextField(blank=True, null=True)
    
    # Optional: Link to originating visit
    originating_visit = models.ForeignKey('VisitLog', on_delete=models.SET_NULL, null=True, blank=True, related_name='generated_leads')
    
    # Value tracking
    estimated_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    actual_value = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    
    # Additional info
    priority = models.CharField(max_length=10, choices=[('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('URGENT', 'Urgent')], default='MEDIUM')
    notes = models.TextField(blank=True, null=True)
    lost_reason = models.TextField(blank=True, null=True, help_text="Reason if status is Lost")
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_leads')
    created_at = models.DateTimeField(auto_now_add=True,editable=True )
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.lead_id:
            # Generate unique lead ID
            last_lead = Lead.objects.order_by('-id').first()
            if last_lead:
                last_id = int(last_lead.lead_id.split('-')[-1])
                self.lead_id = f"LEAD-{last_id + 1:06d}"
            else:
                self.lead_id = "LEAD-000001"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.lead_id} - {self.prospect.name}"
    
    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ['-created_at']


class LeadHistory(models.Model):
    """Track all changes made to leads"""
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='history')
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    field_name = models.CharField(max_length=100)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.lead.lead_id} - {self.field_name} changed"
    
    class Meta:
        verbose_name = "Lead History"
        verbose_name_plural = "Lead Histories"
        ordering = ['-changed_at']


class LeadActivity(models.Model):
    """Activity tracker for lead follow-ups"""
    ACTIVITY_TYPE_CHOICES = [
        ('CALL', 'Phone Call'),
        ('EMAIL', 'Email'),
        ('MEETING', 'Meeting'),
        ('WHATSAPP', 'WhatsApp'),
        ('VISIT', 'Site Visit'),
        ('PROPOSAL', 'Proposal Sent'),
        ('DEMO', 'Product Demo'),
        ('NEGOTIATION', 'Negotiation'),
        ('FOLLOWUP', 'Follow-up'),
        ('OTHER', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('RESCHEDULED', 'Rescheduled'),
    ]
    
    activity_id = models.CharField(max_length=50, unique=True, editable=False)
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    activity_date = models.DateField(default=timezone.now)
    activity_time = models.TimeField(default=timezone.now)
    
    # Discussion details
    discussion_summary = models.TextField(help_text="Summary of discussion and key points")
    outcome = models.TextField(blank=True, null=True, help_text="Outcome of the activity")
    remarks = models.TextField(blank=True, null=True, help_text="Additional remarks or notes")
    
    # Follow-up tracking
    next_followup_date = models.DateField(blank=True, null=True, help_text="Date for next follow-up")
    next_followup_time = models.TimeField(blank=True, null=True, help_text="Time for next follow-up")
    next_action_required = models.TextField(blank=True, null=True, help_text="What needs to be done next")
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COMPLETED')
    lead_status_update = models.CharField(max_length=20, choices=Lead.STATUS_CHOICES, blank=True, null=True, 
                                          help_text="Updated lead status after this activity")
    
    # Attachments
    attachment1 = models.FileField(upload_to='activity_attachments/', blank=True, null=True, 
                                   help_text="Proposal, quote, or other document")
    attachment2 = models.FileField(upload_to='activity_attachments/', blank=True, null=True, 
                                   help_text="Email copy, screenshot, or additional file")
    attachment3 = models.FileField(upload_to='activity_attachments/', blank=True, null=True)
    
    # Contact details
    contact_person = models.CharField(max_length=200, blank=True, null=True, help_text="Person contacted")
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_activities')
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.activity_id:
            # Generate unique activity ID
            last_activity = LeadActivity.objects.order_by('-id').first()
            if last_activity:
                last_id = int(last_activity.activity_id.split('-')[-1])
                self.activity_id = f"ACT-{last_id + 1:06d}"
            else:
                self.activity_id = "ACT-000001"
        super().save(*args, **kwargs)
        
        # Update lead's next action date if this is a future follow-up
        if self.next_followup_date and self.lead:
            if not self.lead.next_action_date or self.next_followup_date < self.lead.next_action_date:
                self.lead.next_action_date = self.next_followup_date
                self.lead.save()
    
    def __str__(self):
        return f"{self.activity_id} - {self.lead.lead_id} - {self.get_activity_type_display()}"
    
    @property
    def is_overdue(self):
        """Check if this is an overdue scheduled activity"""
        if self.status == 'SCHEDULED' and self.activity_date:
            return self.activity_date < timezone.now().date()
        return False
    
    @property
    def is_today(self):
        """Check if this activity is scheduled for today"""
        return self.activity_date == timezone.now().date()
    
    class Meta:
        verbose_name = "Lead Activity"
        verbose_name_plural = "Lead Activities"
        ordering = ['-activity_date', '-activity_time']


class VisitLog(models.Model):
    """Visit log model for tracking sales visits"""
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    OUTCOME_CHOICES = [
        ('POSITIVE', 'Positive'),
        ('NEUTRAL', 'Neutral'),
        ('NEGATIVE', 'Negative'),
        ('DEAL_CLOSED', 'Deal Closed'),
        ('FOLLOW_UP', 'Follow-up Required'),
    ]
    
    APPROVAL_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]
    
    visit_id = models.CharField(max_length=50, unique=True, editable=False)
    sales_employee = models.ForeignKey(SalesEmployee, on_delete=models.CASCADE, related_name='visits')
    prospect = models.ForeignKey(ProspectCustomer, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateField(default=timezone.now)
    visit_time = models.TimeField(default=timezone.now)
    meeting_agenda = models.TextField()
    meeting_outcome = models.TextField(blank=True, null=True)
    outcome_type = models.CharField(max_length=20, choices=OUTCOME_CHOICES, blank=True, null=True)
    next_follow_up_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='COMPLETED')
    approval_status = models.CharField(max_length=20, choices=APPROVAL_CHOICES, default='PENDING')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_visits')
    approved_at = models.DateTimeField(blank=True, null=True)
    
    # Location details
    location = models.CharField(max_length=500, blank=True, null=True)
    gps_latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    gps_longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    
    # Attachments
    visiting_card = models.ImageField(upload_to='visit_attachments/cards/', blank=True, null=True)
    photo = models.ImageField(upload_to='visit_attachments/photos/', blank=True, null=True)
    document = models.FileField(upload_to='visit_attachments/documents/', blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.visit_id:
            # Generate unique visit ID
            last_visit = VisitLog.objects.order_by('-id').first()
            if last_visit:
                last_id = int(last_visit.visit_id.split('-')[-1])
                self.visit_id = f"VST-{last_id + 1:06d}"
            else:
                self.visit_id = "VST-000001"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.visit_id} - {self.prospect.name} by {self.sales_employee.user.username}"
    
    class Meta:
        verbose_name = "Visit Log"
        verbose_name_plural = "Visit Logs"
        ordering = ['-visit_date', '-visit_time']


# ==========================
# QUOTATION MANAGEMENT
# ==========================

class Quotation(models.Model):
    """Quotation/Quote management model"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('SENT', 'Sent to Customer'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
        ('REVISED', 'Revised'),
        ('CONVERTED', 'Converted to Order'),
        ('EXPIRED', 'Expired'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    CURRENCY_CHOICES = [
        ('INR', 'Indian Rupee (₹)'),
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
    ]
    
    # Quote identification
    quote_number = models.CharField(max_length=50, unique=True, editable=False)
    quote_date = models.DateField(default=timezone.now)
    valid_till = models.DateField(help_text="Quotation valid until this date")
    
    # Customer info
    prospect = models.ForeignKey(ProspectCustomer, on_delete=models.CASCADE, related_name='quotations')
    contact_person = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Assignment
    assigned_to = models.ForeignKey(SalesEmployee, on_delete=models.SET_NULL, null=True, related_name='quotations')
    
    # Currency & Exchange
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0000, 
                                       help_text="Exchange rate to base currency")
    
    # Terms & Conditions (can select from master or enter custom)
    payment_terms_master = models.ForeignKey('PaymentTermsMaster', on_delete=models.SET_NULL, 
                                            null=True, blank=True, related_name='quotations',
                                            help_text="Select from Payment Terms Master")
    payment_terms = models.TextField(blank=True, null=True, help_text="Payment terms and conditions")
    delivery_terms_master = models.ForeignKey('DeliveryTermsMaster', on_delete=models.SET_NULL,
                                             null=True, blank=True, related_name='quotations',
                                             help_text="Select from Delivery Terms Master")
    delivery_terms = models.TextField(blank=True, null=True, help_text="Delivery terms and conditions")
    
    # Reference
    reference_lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name='quotations')
    reference_visit = models.ForeignKey(VisitLog, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='quotations')
    reference_number = models.CharField(max_length=100, blank=True, null=True, 
                                       help_text="External reference (PO, RFQ, etc.)")
    
    # Remarks
    customer_remarks = models.TextField(blank=True, null=True, help_text="Remarks visible to customer")
    internal_notes = models.TextField(blank=True, null=True, help_text="Internal notes (not shown to customer)")
    
    # Amounts
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    freight_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Status & workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='approved_quotations')
    approved_at = models.DateTimeField(null=True, blank=True)
    sent_at = models.DateTimeField(null=True, blank=True)
    
    # Order conversion
    converted_to_order = models.BooleanField(default=False)
    order_number = models.CharField(max_length=50, blank=True, null=True)
    order_date = models.DateField(null=True, blank=True)
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_quotations')
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.quote_number:
            # Generate unique quote number
            last_quote = Quotation.objects.order_by('-id').first()
            if last_quote:
                last_id = int(last_quote.quote_number.split('-')[-1])
                self.quote_number = f"QUO-{last_id + 1:06d}"
            else:
                self.quote_number = "QUO-000001"
        super().save(*args, **kwargs)
    
    def calculate_totals(self):
        """Calculate quotation totals from line items"""
        items = self.items.all()
        self.subtotal = sum(item.line_total for item in items)
        self.discount_amount = self.subtotal * (self.discount_percentage / 100)
        taxable_amount = self.subtotal - self.discount_amount
        self.tax_amount = sum(item.tax_amount for item in items)
        self.net_amount = taxable_amount + self.tax_amount + self.freight_charges
        self.save()
    
    @property
    def is_expired(self):
        """Check if quotation has expired"""
        return self.valid_till < timezone.now().date()
    
    @property
    def days_to_expire(self):
        """Days until expiration"""
        if self.is_expired:
            return 0
        delta = self.valid_till - timezone.now().date()
        return delta.days
    
    def __str__(self):
        return f"{self.quote_number} - {self.prospect.name} - ₹{self.net_amount}"
    
    class Meta:
        verbose_name = "Quotation"
        verbose_name_plural = "Quotations"
        ordering = ['-quote_date', '-created_at']


class QuotationItem(models.Model):
    """Line items in a quotation"""
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='items')
    
    # Link to Item Master (optional - allows both master items and custom items)
    item_master = models.ForeignKey('ItemMaster', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='quotation_items', help_text="Select from Item Master")
    
    # Item details (auto-filled from ItemMaster or entered manually)
    item_code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(help_text="Item description")
    
    # Quantity & pricing
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    uom = models.CharField(max_length=20, default='Nos', help_text="Unit of Measurement")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Discount & tax
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Calculated fields
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Sequencing
    line_number = models.IntegerField(default=1)
    
    # Additional info
    remarks = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Calculate line total
        amount = self.quantity * self.unit_price
        discount = amount * (self.discount_percentage / 100)
        taxable = amount - discount
        self.tax_amount = taxable * (self.tax_percentage / 100)
        self.line_total = taxable + self.tax_amount
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quotation.quote_number} - Line {self.line_number}: {self.description}"
    
    class Meta:
        verbose_name = "Quotation Item"
        verbose_name_plural = "Quotation Items"
        ordering = ['quotation', 'line_number']


class QuotationAttachment(models.Model):
    """File attachments for quotations"""
    ATTACHMENT_TYPE_CHOICES = [
        ('PROPOSAL', 'Proposal Document'),
        ('DRAWING', 'Technical Drawing'),
        ('SPECIFICATION', 'Specification'),
        ('BROCHURE', 'Product Brochure'),
        ('TERMS', 'Terms & Conditions'),
        ('OTHER', 'Other'),
    ]
    
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='attachments')
    attachment_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPE_CHOICES, default='OTHER')
    file = models.FileField(upload_to='quotation_attachments/')
    file_name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.file and not self.file_name:
            self.file_name = self.file.name
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.quotation.quote_number} - {self.file_name}"
    
    class Meta:
        verbose_name = "Quotation Attachment"
        verbose_name_plural = "Quotation Attachments"
        ordering = ['-uploaded_at']


class QuotationActivity(models.Model):
    """Activity log for quotations (comments, status changes, etc.)"""
    ACTIVITY_TYPE_CHOICES = [
        ('COMMENT', 'Comment'),
        ('STATUS_CHANGE', 'Status Change'),
        ('SENT', 'Sent to Customer'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('REVISED', 'Revised'),
        ('CONVERTED', 'Converted to Order'),
        ('OTHER', 'Other'),
    ]
    
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField()
    
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    
    is_internal = models.BooleanField(default=True, help_text="Internal activity (not visible to customer)")
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    
    def __str__(self):
        return f"{self.quotation.quote_number} - {self.get_activity_type_display()}"
    
    class Meta:
        verbose_name = "Quotation Activity"
        verbose_name_plural = "Quotation Activities"
        ordering = ['-created_at']


# ==========================
# SALES ORDER MANAGEMENT
# ==========================

class SalesOrder(models.Model):
    """Sales Order management model"""
    STATUS_CHOICES = [
        ('DRAFT', 'Draft'),
        ('PENDING', 'Pending Approval'),
        ('APPROVED', 'Approved'),
        ('CONFIRMED', 'Confirmed'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    CURRENCY_CHOICES = [
        ('INR', 'Indian Rupee (₹)'),
        ('USD', 'US Dollar ($)'),
        ('EUR', 'Euro (€)'),
        ('GBP', 'British Pound (£)'),
    ]
    
    # Order identification
    order_number = models.CharField(max_length=50, unique=True, editable=False)
    order_date = models.DateField(default=timezone.now)
    valid_till = models.DateField(help_text="Order valid until this date")
    
    # Customer info
    prospect = models.ForeignKey(ProspectCustomer, on_delete=models.CASCADE, related_name='orders')
    contact_person = models.CharField(max_length=200)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    
    # Assignment
    assigned_to = models.ForeignKey(SalesEmployee, on_delete=models.SET_NULL, null=True, related_name='orders')
    
    # Currency & Exchange
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR')
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=4, default=1.0000, 
                                       help_text="Exchange rate to base currency")
    
    # Terms & Conditions (can select from master or enter custom)
    payment_terms_master = models.ForeignKey('PaymentTermsMaster', on_delete=models.SET_NULL, 
                                            null=True, blank=True, related_name='orders',
                                            help_text="Select from Payment Terms Master")
    payment_terms = models.TextField(blank=True, null=True, help_text="Payment terms and conditions")
    delivery_terms_master = models.ForeignKey('DeliveryTermsMaster', on_delete=models.SET_NULL,
                                             null=True, blank=True, related_name='orders',
                                             help_text="Select from Delivery Terms Master")
    delivery_terms = models.TextField(blank=True, null=True, help_text="Delivery terms and conditions")
    
    # Reference
    reference_lead = models.ForeignKey(Lead, on_delete=models.SET_NULL, null=True, blank=True, 
                                      related_name='orders')
    reference_visit = models.ForeignKey(VisitLog, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='orders')
    reference_quotation = models.ForeignKey(Quotation, on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='converted_orders')
    reference_number = models.CharField(max_length=100, blank=True, null=True, 
                                       help_text="External reference (PO, RFQ, etc.)")
    
    # Remarks
    customer_remarks = models.TextField(blank=True, null=True, help_text="Remarks visible to customer")
    internal_notes = models.TextField(blank=True, null=True, help_text="Internal notes (not shown to customer)")
    
    # Amounts
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    freight_charges = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Status & workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='approved_orders')
    approved_at = models.DateTimeField(null=True, blank=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    shipped_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders')
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate unique order number
            last_order = SalesOrder.objects.order_by('-id').first()
            if last_order:
                last_id = int(last_order.order_number.split('-')[-1])
                self.order_number = f"SO-{last_id + 1:06d}"
            else:
                self.order_number = "SO-000001"
        super().save(*args, **kwargs)
    
    def calculate_totals(self):
        """Calculate order totals from line items"""
        items = self.items.all()
        self.subtotal = sum(item.line_total for item in items)
        self.discount_amount = self.subtotal * (self.discount_percentage / 100)
        taxable_amount = self.subtotal - self.discount_amount
        self.tax_amount = sum(item.tax_amount for item in items)
        self.net_amount = taxable_amount + self.tax_amount + self.freight_charges
        self.save()
    
    @property
    def is_expired(self):
        """Check if order has expired"""
        return self.valid_till < timezone.now().date()
    
    @property
    def days_to_expire(self):
        """Days until expiration"""
        if self.is_expired:
            return 0
        delta = self.valid_till - timezone.now().date()
        return delta.days
    
    def __str__(self):
        return f"{self.order_number} - {self.prospect.name} - ₹{self.net_amount}"
    
    class Meta:
        verbose_name = "Sales Order"
        verbose_name_plural = "Sales Orders"
        ordering = ['-order_date', '-created_at']


class SalesOrderItem(models.Model):
    """Line items in a sales order"""
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='items')
    
    # Link to Item Master (optional - allows both master items and custom items)
    item_master = models.ForeignKey('ItemMaster', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='order_items', help_text="Select from Item Master")
    
    # Item details (auto-filled from ItemMaster or entered manually)
    item_code = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(help_text="Item description")
    
    # Quantity & pricing
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1)
    uom = models.CharField(max_length=20, default='Nos', help_text="Unit of Measurement")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    
    # Discount & tax
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    
    # Calculated fields
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Sequencing
    line_number = models.IntegerField(default=1)
    
    # Additional info
    remarks = models.TextField(blank=True, null=True)
    
    def save(self, *args, **kwargs):
        # Calculate line total
        amount = self.quantity * self.unit_price
        discount = amount * (self.discount_percentage / 100)
        taxable = amount - discount
        self.tax_amount = taxable * (self.tax_percentage / 100)
        self.line_total = taxable + self.tax_amount
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order.order_number} - Line {self.line_number}: {self.description}"
    
    class Meta:
        verbose_name = "Sales Order Item"
        verbose_name_plural = "Sales Order Items"
        ordering = ['order', 'line_number']


class SalesOrderAttachment(models.Model):
    """File attachments for sales orders"""
    ATTACHMENT_TYPE_CHOICES = [
        ('PROPOSAL', 'Proposal Document'),
        ('DRAWING', 'Technical Drawing'),
        ('SPECIFICATION', 'Specification'),
        ('BROCHURE', 'Product Brochure'),
        ('TERMS', 'Terms & Conditions'),
        ('OTHER', 'Other'),
    ]
    
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='attachments')
    attachment_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPE_CHOICES, default='OTHER')
    file = models.FileField(upload_to='order_attachments/')
    file_name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, blank=True, null=True)
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if self.file and not self.file_name:
            self.file_name = self.file.name
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.order.order_number} - {self.file_name}"
    
    class Meta:
        verbose_name = "Sales Order Attachment"
        verbose_name_plural = "Sales Order Attachments"
        ordering = ['-uploaded_at']


class SalesOrderActivity(models.Model):
    """Activity log for sales orders (comments, status changes, etc.)"""
    ACTIVITY_TYPE_CHOICES = [
        ('COMMENT', 'Comment'),
        ('STATUS_CHANGE', 'Status Change'),
        ('CONFIRMED', 'Confirmed'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('OTHER', 'Other'),
    ]
    
    order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    description = models.TextField()
    
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    
    is_internal = models.BooleanField(default=True, help_text="Internal activity (not visible to customer)")
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    
    def __str__(self):
        return f"{self.order.order_number} - {self.get_activity_type_display()}"
    
    class Meta:
        verbose_name = "Sales Order Activity"
        verbose_name_plural = "Sales Order Activities"
        ordering = ['-created_at']


# =====================================================
# MASTER DATA MANAGEMENT
# =====================================================

class ItemMaster(models.Model):
    """Product/Service Master for inventory and sales"""
    ITEM_TYPE_CHOICES = [
        ('PRODUCT', 'Product'),
        ('SERVICE', 'Service'),
        ('CONSUMABLE', 'Consumable'),
    ]
    
    item_code = models.CharField(max_length=50, unique=True, db_index=True)
    description = models.TextField()
    short_name = models.CharField(max_length=200, blank=True, null=True)
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES, default='PRODUCT')
    unit_of_measurement = models.CharField(max_length=20, default='PCS', help_text="e.g., PCS, KG, LTR, MTR")
    
    # Pricing
    standard_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    minimum_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, help_text="Minimum selling price")
    purchase_price = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, blank=True, null=True)
    
    # Tax
    hsn_sac_code = models.CharField(max_length=20, blank=True, null=True, help_text="HSN/SAC code for GST")
    default_tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, help_text="Default GST %")
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Additional info
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    brand = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    remarks = models.TextField(blank=True, null=True)
    
    # Tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_items')
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.item_code} - {self.description[:50]}"
    
    class Meta:
        verbose_name = "Item Master"
        verbose_name_plural = "Item Masters"
        ordering = ['item_code']


class TaxMaster(models.Model):
    """Tax Master for GST and other taxes"""
    TAX_TYPE_CHOICES = [
        ('GST', 'GST'),
        ('IGST', 'IGST'),
        ('CGST', 'CGST'),
        ('SGST', 'SGST'),
        ('CESS', 'CESS'),
        ('OTHER', 'Other'),
    ]
    
    tax_code = models.CharField(max_length=50, unique=True, db_index=True)
    tax_name = models.CharField(max_length=200)
    tax_type = models.CharField(max_length=20, choices=TAX_TYPE_CHOICES)
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    hsn_sac_code = models.CharField(max_length=20, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.tax_code} - {self.tax_name} ({self.tax_percentage}%)"
    
    class Meta:
        verbose_name = "Tax Master"
        verbose_name_plural = "Tax Masters"
        ordering = ['tax_code']


class PaymentTermsMaster(models.Model):
    """Payment Terms Master"""
    term_code = models.CharField(max_length=50, unique=True, db_index=True)
    term_name = models.CharField(max_length=200)
    days = models.IntegerField(help_text="Number of days for payment")
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.term_code} - {self.term_name} ({self.days} days)"
    
    class Meta:
        verbose_name = "Payment Terms"
        verbose_name_plural = "Payment Terms"
        ordering = ['term_code']


class DeliveryTermsMaster(models.Model):
    """Delivery Terms Master - INCO Terms"""
    INCO_TERMS_CHOICES = [
        ('EXW', 'Ex Works'),
        ('FCA', 'Free Carrier'),
        ('CPT', 'Carriage Paid To'),
        ('CIP', 'Carriage and Insurance Paid To'),
        ('DAP', 'Delivered at Place'),
        ('DPU', 'Delivered at Place Unloaded'),
        ('DDP', 'Delivered Duty Paid'),
        ('FAS', 'Free Alongside Ship'),
        ('FOB', 'Free on Board'),
        ('CFR', 'Cost and Freight'),
        ('CIF', 'Cost, Insurance and Freight'),
    ]
    
    term_code = models.CharField(max_length=50, unique=True, db_index=True)
    term_name = models.CharField(max_length=200)
    inco_term = models.CharField(max_length=10, choices=INCO_TERMS_CHOICES, blank=True, null=True)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.term_code} - {self.term_name}"
    
    class Meta:
        verbose_name = "Delivery Terms"
        verbose_name_plural = "Delivery Terms"
        ordering = ['term_code']


class VisitPurposeMaster(models.Model):
    """Visit Purpose Master for categorizing customer visits"""
    purpose_code = models.CharField(max_length=50, unique=True, db_index=True)
    purpose_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.purpose_code} - {self.purpose_name}"
    
    class Meta:
        verbose_name = "Visit Purpose"
        verbose_name_plural = "Visit Purposes"
        ordering = ['purpose_code']


class ApprovalMatrix(models.Model):
    """Approval Matrix for quotations and orders based on value"""
    DOCUMENT_TYPE_CHOICES = [
        ('QUOTATION', 'Quotation'),
        ('SALES_ORDER', 'Sales Order'),
        ('DISCOUNT', 'Discount Approval'),
    ]
    
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPE_CHOICES)
    min_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2, help_text="Use 999999999 for unlimited")
    approver_role = models.CharField(max_length=100, help_text="Role required for approval (e.g., Sales Manager, Director)")
    approver = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='approval_matrix', help_text="Specific approver (optional)")
    remarks = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.document_type} - {self.min_amount} to {self.max_amount} - {self.approver_role}"
    
    class Meta:
        verbose_name = "Approval Matrix"
        verbose_name_plural = "Approval Matrices"
        ordering = ['document_type', 'min_amount']


# =====================================================
# SERVICE CALL MANAGEMENT SYSTEM
# =====================================================

class Technician(models.Model):
    """Service technicians/engineers master"""
    SKILL_LEVEL_CHOICES = [
        ('TRAINEE', 'Trainee'),
        ('JUNIOR', 'Junior Technician'),
        ('SENIOR', 'Senior Technician'),
        ('SPECIALIST', 'Specialist'),
        ('LEAD', 'Lead Engineer'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='technician_profile')
    employee_code = models.CharField(max_length=50, unique=True, db_index=True, 
                                    help_text="Unique technician employee code (e.g., TECH-00001)")
    mobile = models.CharField(max_length=15)
    alternate_mobile = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField()
    alternate_email = models.EmailField(blank=True, null=True)
    
    # Professional Details
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVEL_CHOICES, default='JUNIOR')
    specialization = models.CharField(max_length=200, blank=True, null=True, 
                                     help_text="E.g., Pumps, Motors, HVAC, Electronics, Automation")
    
    # Location & Territory
    region = models.CharField(max_length=100, blank=True, null=True)
    territory = models.ForeignKey(Territory, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='technicians')
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    
    # Employment Details
    joining_date = models.DateField(default=timezone.now, help_text="Date when technician joined")
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name='technicians')
    designation = models.ForeignKey(Designation, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='technicians')
    reporting_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='subordinates', help_text="Senior technician/manager")
    
    # Availability & Status
    is_active = models.BooleanField(default=True)
    is_available = models.BooleanField(default=True, help_text="Currently available for service calls")
    
    # Additional Info
    emergency_contact_name = models.CharField(max_length=200, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=15, blank=True, null=True)
    aadhar_number = models.CharField(max_length=12, blank=True, null=True)
    pan_number = models.CharField(max_length=10, blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True,
                                     help_text="Driving license or professional license")
    notes = models.TextField(blank=True, null=True, help_text="Additional notes or remarks")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        """Auto-generate employee code if not exists"""
        if not self.employee_code:
            last_tech = Technician.objects.order_by('-id').first()
            if last_tech and last_tech.employee_code:
                try:
                    last_num = int(last_tech.employee_code.split('-')[-1])
                    self.employee_code = f"TECH-{last_num + 1:05d}"
                except (ValueError, IndexError):
                    self.employee_code = "TECH-00001"
            else:
                self.employee_code = "TECH-00001"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.employee_code} - {self.user.get_full_name() or self.user.username}"
    
    @property
    def full_name(self):
        """Return full name of technician"""
        return self.user.get_full_name() or self.user.username
    
    @property
    def active_service_calls_count(self):
        """Count of active service calls assigned to this technician"""
        return self.assigned_calls.filter(status__in=['NEW', 'ASSIGNED', 'SCHEDULED', 'IN_PROGRESS']).count()
    
    class Meta:
        verbose_name = "Technician"
        verbose_name_plural = "Technicians"
        ordering = ['employee_code']


class ServiceContract(models.Model):
    """AMC/Service Contracts"""
    CONTRACT_TYPE_CHOICES = [
        ('AMC', 'Annual Maintenance Contract'),
        ('CMC', 'Comprehensive Maintenance Contract'),
        ('WARRANTY', 'Extended Warranty'),
        ('ONETIME', 'One-time Service Package'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('SUSPENDED', 'Suspended'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    contract_number = models.CharField(max_length=50, unique=True, editable=False)
    customer = models.ForeignKey(ProspectCustomer, on_delete=models.CASCADE, related_name='service_contracts')
    related_order = models.ForeignKey(SalesOrder, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='service_contracts')
    
    contract_type = models.CharField(max_length=20, choices=CONTRACT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    contract_value = models.DecimalField(max_digits=12, decimal_places=2)
    
    service_frequency = models.CharField(max_length=100, blank=True, null=True,
                                        help_text="E.g., Quarterly, Monthly")
    number_of_visits = models.IntegerField(default=0, help_text="Total visits included")
    visits_completed = models.IntegerField(default=0)
    
    coverage_details = models.TextField(blank=True, null=True)
    exclusions = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ACTIVE')
    
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_contracts')
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.contract_number:
            # Auto-generate contract number
            last_contract = ServiceContract.objects.order_by('-id').first()
            if last_contract and last_contract.contract_number:
                last_num = int(last_contract.contract_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1
            self.contract_number = f"AMC-{timezone.now().year}-{new_num:05d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.contract_number} - {self.customer.name}"
    
    class Meta:
        verbose_name = "Service Contract"
        verbose_name_plural = "Service Contracts"
        ordering = ['-start_date']


class WarrantyRecord(models.Model):
    """Warranty records for products"""
    WARRANTY_TYPE_CHOICES = [
        ('MANUFACTURER', 'Manufacturer Warranty'),
        ('DEALER', 'Dealer Warranty'),
        ('EXTENDED', 'Extended Warranty'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('EXPIRED', 'Expired'),
        ('CLAIMED', 'Claimed'),
        ('VOID', 'Void'),
    ]
    
    warranty_number = models.CharField(max_length=50, unique=True)
    customer = models.ForeignKey(ProspectCustomer, on_delete=models.CASCADE, related_name='warranties')
    related_order = models.ForeignKey(SalesOrder, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='warranties')
    
    product_serial_number = models.CharField(max_length=100, blank=True, null=True)
    product_description = models.TextField()
    
    warranty_type = models.CharField(max_length=20, choices=WARRANTY_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    
    coverage_details = models.TextField(blank=True, null=True)
    terms_conditions = models.TextField(blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW')
    
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(null=True, blank=True, )
    
    def __str__(self):
        return f"{self.warranty_number} - {self.product_description[:50]}"
    
    class Meta:
        verbose_name = "Warranty Record"
        verbose_name_plural = "Warranty Records"
        ordering = ['-start_date']


class ServiceCall(models.Model):
    """Service Call/Ticket Header"""
    SERVICE_TYPE_CHOICES = [
        ('BREAKDOWN', 'Breakdown'),
        ('PREVENTIVE', 'Preventive Maintenance'),
        ('INSTALLATION', 'Installation'),
        ('CALIBRATION', 'Calibration'),
        ('WARRANTY', 'Warranty Claim'),
        ('AMC', 'AMC Service'),
        ('INSPECTION', 'Inspection'),
        ('TRAINING', 'Training'),
    ]
    
    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('CLOSED', 'Closed'),
    ]
    
    MODE_CHOICES = [
        ('ONSITE', 'Onsite Visit'),
        ('REMOTE', 'Remote Support'),
        ('PHONE', 'Phone Support'),
        ('EMAIL', 'Email Support'),
        ('REMOTE_ACCESS', 'Remote Access'),
    ]
    
    WARRANTY_STATUS_CHOICES = [
        ('UNDER_WARRANTY', 'Under Warranty'),
        ('OUT_OF_WARRANTY', 'Out of Warranty'),
        ('AMC', 'Under AMC'),
        ('PAID', 'Paid Service'),
    ]
    
    RESOLUTION_CODE_CHOICES = [
        ('RESOLVED', 'Successfully Resolved'),
        ('PARTIAL', 'Partially Resolved'),
        ('PENDING_PARTS', 'Pending Spare Parts'),
        ('ESCALATED', 'Escalated'),
        ('CUSTOMER_DECLINED', 'Customer Declined'),
        ('NOT_RESOLVED', 'Not Resolved'),
    ]

    ORIGIN_CHOICES = [
        ('PHONE', 'Phone'),
        ('EMAIL', 'Email'),
        ('WHATSAPP', 'WhatsApp'),
        ('PORTAL', 'Customer Portal'),
        ('VISIT', 'Site Visit'),
    ]

    CALL_TYPE_CHOICES = [
        ('BREAKDOWN', 'Breakdown'),
        ('SERVICE', 'Service'),
        ('INSTALLATION', 'Installation'),
    ]
    CALL_TYPE_CHOICES = [
    ('BREAKDOWN', 'Breakdown'),
    ('SERVICE', 'Service'),
    ('INSTALLATION', 'Installation'),
]

    call_type = models.CharField(
    max_length=20,
    choices=CALL_TYPE_CHOICES,
    default='SERVICE'   # ✅ IMPORTANT
    )


    PROBLEM_TYPE_CHOICES = [
        ('MECHANICAL', 'Mechanical'),
        ('ELECTRICAL', 'Electrical'),
        ('SOFTWARE', 'Software'),
        ('OTHER', 'Other'),
    ]

    origin = models.CharField(
        max_length=20,
        choices=ORIGIN_CHOICES,
        default='PHONE'
    )

    problem_type = models.CharField(
        max_length=20,
        choices=PROBLEM_TYPE_CHOICES,
        default='OTHER'
    )



    assigned_technician = models.ForeignKey(
        Technician,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_calls'
    )

    
    # Service Call Identification
    service_number = models.CharField(max_length=50, unique=True, editable=True)
    
    item_name = models.CharField(
    max_length=20,
    blank=True,
    null=True,
    help_text="Equipment / Item name"
    )

    serial_number = models.CharField(
    max_length=200,
    blank=True,
    null=True,
    help_text="Equipment serial number"
    )

    # status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='NEW'
    )
    
    # Related Documents
    related_order = models.ForeignKey(SalesOrder, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='service_calls')
    related_quotation = models.ForeignKey(Quotation, on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='service_calls')
    
    # Customer Information
    customer = models.ForeignKey(ProspectCustomer, on_delete=models.CASCADE, related_name='service_calls')
    contact_person = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=10)
    contact_email = models.EmailField(blank=True, null=True)
    
    # Service Request Details
    service_request_date = models.DateTimeField(default=timezone.now)
    preferred_visit_date = models.DateTimeField(null=True, blank=True)
    
    # Assignment
    assigned_technician = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True, blank=True,related_name='assigned_calls')
    assigned_team = models.CharField(max_length=100, blank=True, null=True,help_text="Region/Shift/Team")
    
    # Service Details
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='MEDIUM')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='ONSITE')
    
    # Problem Details
    fault_category = models.CharField(max_length=100, blank=True, null=True)
    symptom = models.CharField(max_length=200, blank=True, null=True)
    equipment_details = models.TextField(
        blank=True,
        null=True,
        help_text="Make/model/serial information for the equipment"
    )
    problem_description = models.TextField(help_text="Customer's description of the issue")
    diagnosis_summary = models.TextField(blank=True, null=True, help_text="Technician's diagnosis")
    resolution_summary = models.TextField(blank=True, null=True, help_text="Final resolution")
    root_cause = models.TextField(blank=True, null=True)
    
    # Parts & Warranty
    parts_required = models.BooleanField(default=False)
    warranty_status = models.CharField(max_length=20, choices=WARRANTY_STATUS_CHOICES, default='PAID')
    warranty_record = models.ForeignKey(WarrantyRecord, on_delete=models.SET_NULL, null=True, blank=True,related_name='service_calls')
    service_contract = models.ForeignKey(ServiceContract, on_delete=models.SET_NULL, null=True, blank=True,related_name='service_calls')
    
    # Resolution
    resolution_code = models.CharField(max_length=30, choices=RESOLUTION_CODE_CHOICES, blank=True, null=True)
    
    # Time Tracking
    time_spent_minutes = models.IntegerField(default=0, help_text="Actual service time in minutes")
    service_duration = models.DurationField(null=True, blank=True)
    travel_time_minutes = models.IntegerField(default=0, help_text="Travel time for onsite visits")
    travel_distance_km = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, blank=True, null=True)
    
    # Closure
    call_closed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='closed_service_calls')
    closed_at = models.DateTimeField(null=True, blank=True)
    
    # Customer Feedback
    customer_feedback_rating = models.IntegerField(null=True, blank=True, 
                                                   help_text="Rating 1-5")
    customer_feedback_comments = models.TextField(blank=True, null=True)
    
    # Follow-up
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateTimeField(null=True, blank=True)
    
    # Billing
    billable = models.BooleanField(default=True)
    estimated_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    actual_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    invoice_number = models.CharField(max_length=50, blank=True, null=True)
    
    # Additional Info
    attachments_path = models.TextField(blank=True, null=True, help_text="Comma-separated file paths")
    internal_notes = models.TextField(blank=True, null=True)
    
    # Audit Fields
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_service_calls')
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    closed_at = models.DateTimeField(blank=True, null=True, editable=True)

    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,related_name='updated_service_calls')
    updated_at = models.DateTimeField(auto_now=True)
    
def save(self, *args, **kwargs):
    # 1️⃣ Auto-generate service number
    if not self.service_number:
        year = timezone.now().year
        last_call = ServiceCall.objects.filter(
            service_number__startswith=f"SVC-{year}"
        ).order_by('-id').first()

        last_num = int(last_call.service_number.split('-')[-1]) if last_call else 0
        self.service_number = f"SVC-{year}-{last_num + 1:04d}"

    # 2️⃣ Auto set closed_at when status is CLOSED
    if self.status == 'CLOSED':
        if self.closed_at is None:
            self.closed_at = timezone.now()
    else:
        # Clear closed_at if reopened
        self.closed_at = None

    super().save(*args, **kwargs)
class ServiceCallItem(models.Model):
    """Line items for parts/products used in service call"""
    service_call = models.ForeignKey(ServiceCall, on_delete=models.CASCADE, related_name='items')
    
    # Item details
    item_master = models.ForeignKey(ItemMaster, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='service_items')
    item_code = models.CharField(max_length=100, blank=True, null=True)
    product_serial_no = models.CharField(max_length=100, blank=True, null=True,
                                         help_text="Product's serial number if fielded")
    description = models.TextField()
    fault_found = models.TextField(blank=True, null=True, 
                                   help_text="Description of fault found in this item")
    
    # Quantity & Type
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=1,
                                   help_text="Quantity of spare parts used")
    uom = models.CharField(max_length=20, default='Nos')
    
    item_type = models.CharField(max_length=20, choices=[
        ('SPARE_PART', 'Spare Part'),
        ('CONSUMABLE', 'Consumable'),
        ('SERVICE', 'Service Charge'),
        ('TRAVEL', 'Travel Charge'),
    ], default='SPARE_PART')
    
    # Pricing (unit_cost / unit_price)
    unit_cost = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,
                                    help_text="Cost price")
    unit_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,
                                     help_text="Selling price")
    
    # Labour charges
    labour_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0.00,
                                      help_text="Labour hours for this item")
    labour_rate = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                     help_text="Labour rate per hour")
    
    # Tax and totals
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    line_total = models.DecimalField(max_digits=12, decimal_places=2, default=0.00,
                                     help_text="Total including parts, labour, and tax")
    
    # Warranty & Traceability
    warranty_covered = models.BooleanField(default=False, help_text="Covered under warranty (Y/N)")
    batch_no = models.CharField(max_length=100, blank=True, null=True,
                                help_text="Batch number for traceability")
    serial_number = models.CharField(max_length=100, blank=True, null=True,
                                    help_text="Serial number for traceability")
    
    # Additional Info
    remarks = models.TextField(blank=True, null=True)
    line_number = models.IntegerField(default=1)
    
    def save(self, *args, **kwargs):
        # Calculate line total: (parts + labour) + tax
        parts_amount = self.quantity * self.unit_price
        labour_amount = self.labour_hours * self.labour_rate
        subtotal = parts_amount + labour_amount
        tax_amount = subtotal * (self.tax_percentage / 100)
        self.line_total = subtotal + tax_amount
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.service_call.service_number} - Line {self.line_number} - {self.description[:50]}"
    
    class Meta:
        verbose_name = "Service Call Item"
        verbose_name_plural = "Service Call Items"
        ordering = ['service_call', 'line_number']


class ServiceActivity(models.Model):
    """Activities/Tasks performed during service call"""
    ACTIVITY_TYPE_CHOICES = [
        ('DIAGNOSIS', 'Diagnosis'),
        ('REPAIR', 'Repair'),
        ('REPLACEMENT', 'Part Replacement'),
        ('CLEANING', 'Cleaning'),
        ('CALIBRATION', 'Calibration'),
        ('TESTING', 'Testing'),
        ('TRAINING', 'Training'),
        ('CONSULTATION', 'Consultation'),
        ('TRAVEL', 'Travel'),
        ('OTHER', 'Other'),
    ]
    
    service_call = models.ForeignKey(ServiceCall, on_delete=models.CASCADE, related_name='activities')
    
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_TYPE_CHOICES)
    activity_date = models.DateField(default=timezone.now)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(default=0)
    
    description = models.TextField()
    performed_by = models.ForeignKey(Technician, on_delete=models.SET_NULL, null=True,
                                    related_name='service_activities')
    
    remarks = models.TextField(blank=True, null=True)
    is_billable = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    
    def __str__(self):
        return f"{self.service_call.service_number} - {self.activity_type} - {self.activity_date}"
    
    class Meta:
        verbose_name = "Service Activity"
        verbose_name_plural = "Service Activities"
        ordering = ['service_call', 'activity_date', 'start_time']


class ServiceCallAttachment(models.Model):
    """Attachments for service calls (images, documents, logs)"""
    ATTACHMENT_TYPE_CHOICES = [
        ('IMAGE', 'Image'),
        ('DOCUMENT', 'Document'),
        ('LOG', 'Log File'),
        ('REPORT', 'Report'),
        ('OTHER', 'Other'),
    ]

    service_call = models.ForeignKey(ServiceCall, on_delete=models.CASCADE, related_name='attachments')

    file = models.FileField(upload_to='service_call_attachments/%Y/%m/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=20, choices=ATTACHMENT_TYPE_CHOICES)
    file_size = models.IntegerField(help_text="Size in bytes")

    description = models.TextField(blank=True, null=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_call.service_number} - {self.file_name}"

    class Meta:
        verbose_name = "Service Call Attachment"
        verbose_name_plural = "Service Call Attachments"
        ordering = ['-uploaded_at']


class SpareUsage(models.Model):
    """Spare Parts Usage / Inventory Tracking"""
    service_call = models.ForeignKey(ServiceCall, on_delete=models.CASCADE, related_name='spare_usage')
    part = models.ForeignKey(ItemMaster, on_delete=models.CASCADE, related_name='spare_usage_records')

    qty_used = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity of spare parts used")
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Cost price per unit")
    sell_price = models.DecimalField(max_digits=12, decimal_places=2, help_text="Selling price per unit")

    warehouse_id = models.CharField(max_length=50, blank=True, null=True, help_text="Source warehouse/store")

    replacement_reason = models.CharField(max_length=100, choices=[
        ('WARRANTY', 'Warranty Replacement'),
        ('WEAR_AND_TEAR', 'Wear and Tear'),
        ('DAMAGE', 'Damage/Malfunction'),
        ('UPGRADE', 'Upgrade/Improvement'),
        ('OTHER', 'Other'),
    ], default='OTHER')

    technician_remarks = models.TextField(blank=True, null=True)
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                   related_name='verified_spare_usage', help_text="Inventory manager verification")
    verified_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,editable=True)

    def __str__(self):
        return f"{self.service_call.service_number} - {self.part.item_code} - Qty: {self.qty_used}"

    class Meta:
        verbose_name = "Spare Parts Usage"
        verbose_name_plural = "Spare Parts Usage Records"
        ordering = ['-created_at']


class ServiceInvoice(models.Model):
    """Service Invoice / Billing"""
    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PART_PAID', 'Partially Paid'),
        ('PAID', 'Paid'),
        ('OVERDUE', 'Overdue'),
        ('CANCELLED', 'Cancelled'),
    ]

    PAYMENT_MODE_CHOICES = [
        ('CASH', 'Cash'),
        ('CHEQUE', 'Cheque'),
        ('ONLINE', 'Online Transfer'),
        ('CARD', 'Card Payment'),
        ('OTHER', 'Other'),
    ]

    service_invoice_id = models.CharField(max_length=50, unique=True)
    service_call = models.OneToOneField(ServiceCall, on_delete=models.CASCADE, related_name='service_invoice')

    invoice_number = models.CharField(max_length=50, unique=True, editable=False)
    invoice_date = models.DateField(default=timezone.now)

    # Amount breakdown
    amount_parts = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    amount_labour = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    amount_travel = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    taxes = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # Payment tracking
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, blank=True, null=True)
    receipt_no = models.CharField(max_length=50, blank=True, null=True)

    # Linking to accounting/finance
    linked_accounting_doc = models.CharField(max_length=100, blank=True, null=True,
                                            help_text="Reference to SAP B1 or finance system")

    # Due dates and terms
    due_date = models.DateField(null=True, blank=True)
    payment_terms = models.TextField(blank=True, null=True)

    # Audit and additional info
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_invoices')
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Generate invoice number: SVC-INV-YYYY-0001
            year = timezone.now().year
            last_invoice = ServiceInvoice.objects.filter(
                invoice_number__startswith=f'SVC-INV-{year}'
            ).order_by('-id').first()

            if last_invoice and last_invoice.invoice_number:
                last_num = int(last_invoice.invoice_number.split('-')[-1])
                new_num = last_num + 1
            else:
                new_num = 1

            self.invoice_number = f'SVC-INV-{year}-{new_num:04d}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.invoice_number} - {self.service_call.service_number}"

    class Meta:
        verbose_name = "Service Invoice"
        verbose_name_plural = "Service Invoices"
        ordering = ['-invoice_date']


# =====================================
# Additional Service Master Data
# =====================================

class FaultCategory(models.Model):
    """Fault Category Master for service calls"""
    category_code = models.CharField(max_length=50, unique=True, db_index=True)
    category_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    service_types = models.CharField(max_length=500, blank=True, null=True,
                                    help_text="Comma-separated applicable service types")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.category_code} - {self.category_name}"

    class Meta:
        verbose_name = "Fault Category"
        verbose_name_plural = "Fault Categories"
        ordering = ['category_code']


class SymptomMaster(models.Model):
    """Symptom Master for common symptoms"""
    symptom_code = models.CharField(max_length=50, unique=True, db_index=True)
    symptom_name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    fault_categories = models.ManyToManyField(FaultCategory, blank=True, related_name='symptoms')
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.symptom_code} - {self.symptom_name}"

    class Meta:
        verbose_name = "Symptom"
        verbose_name_plural = "Symptoms"
        ordering = ['symptom_code']


class SLAConfig(models.Model):
    """SLA Configuration for service response and resolution times"""
    SERVICE_TYPE_CHOICES = [
        ('BREAKDOWN', 'Breakdown'),
        ('PREVENTIVE', 'Preventive Maintenance'),
        ('INSTALLATION', 'Installation'),
        ('CALIBRATION', 'Calibration'),
        ('WARRANTY', 'Warranty Claim'),
        ('AMC', 'AMC Service'),
        ('ALL', 'All Service Types'),
    ]

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('CRITICAL', 'Critical'),
        ('ALL', 'All Priorities'),
    ]

    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='ALL')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='ALL')

    response_time_sla_hours = models.IntegerField(default=24, help_text="Response time in hours")
    resolution_time_sla_hours = models.IntegerField(default=72, help_text="Resolution time in hours")

    business_hours_only = models.BooleanField(default=True)
    escalation_threshold_percentage = models.IntegerField(default=80,
                                                         help_text="Percentage of SLA time for escalation warning")

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True,editable=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"SLA - {self.get_service_type_display()} / {self.get_priority_display()}"

    class Meta:
        verbose_name = "SLA Configuration"
        verbose_name_plural = "SLA Configurations"
        ordering = ['service_type', 'priority']
