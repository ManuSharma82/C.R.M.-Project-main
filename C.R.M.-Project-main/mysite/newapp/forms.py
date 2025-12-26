from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory
from .models import (ProspectCustomer, VisitLog, SalesEmployee, Lead, LeadActivity,
                     Quotation, QuotationItem, QuotationAttachment, QuotationActivity,
                     SalesOrder, SalesOrderItem, SalesOrderAttachment, SalesOrderActivity,
                     ServiceCall, ServiceCallItem, ServiceCallAttachment, ServiceActivity,
                     Technician, WarrantyRecord, ServiceContract)


class CustomSignUpForm(UserCreationForm):
    """Custom signup form with enhanced styling and validation"""
    
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Choose a username',
            'autocomplete': 'username',
        })
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'your.email@example.com',
            'autocomplete': 'email',
        })
    )
    
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Create a strong password',
            'autocomplete': 'new-password',
        })
    )
    
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Confirm your password',
            'autocomplete': 'new-password',
        })
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomSignInForm(AuthenticationForm):
    """Custom sign-in form with enhanced styling - accepts username or email"""
    
    username = forms.CharField(
        label='Username or Email',
        max_length=254,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your username or email',
            'autocomplete': 'username',
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your password',
            'autocomplete': 'current-password',
        })
    )
    
    def clean_username(self):
        """Allow login with email or username"""
        username_or_email = self.cleaned_data.get('username')
        
        # Check if input is an email address
        if '@' in username_or_email:
            try:
                # Try to find user by email
                user = User.objects.get(email=username_or_email)
                return user.username
            except User.DoesNotExist:
                # Return the original input to let Django's auth handle the error
                return username_or_email
        
        # Return username as-is
        return username_or_email


class ProspectCustomerForm(forms.ModelForm):
    """Form for creating and updating prospect/customer records"""
    
    class Meta:
        model = ProspectCustomer
        fields = [
            'name', 'company_name', 'type', 'status', 'email', 'phone', 
            'alternate_phone', 'address', 'city', 'state', 'pincode',
            'latitude', 'longitude', 'industry', 'assigned_to', 'notes'
        ]
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter contact person name'
            }),
            'company_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter company name'
            }),
            'type': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'email@example.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+91 XXXXXXXXXX'
            }),
            'alternate_phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Alternate phone (optional)'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Full address',
                'rows': 3
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'City'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'State'
            }),
            'pincode': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Pincode'
            }),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Latitude (optional)',
                'step': '0.000001'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Longitude (optional)',
                'step': '0.000001'
            }),
            'industry': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Industry type'
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Additional notes',
                'rows': 3
            }),
        }


class VisitLogForm(forms.ModelForm):
    """Form for creating and updating visit logs"""
    
    class Meta:
        model = VisitLog
        fields = [
            'prospect', 'visit_date', 'visit_time', 'meeting_agenda',
            'meeting_outcome', 'outcome_type', 'next_follow_up_date',
            'status', 'location', 'gps_latitude', 'gps_longitude',
            'visiting_card', 'photo', 'document'
        ]
        widgets = {
            'prospect': forms.Select(attrs={
                'class': 'form-input',
                'required': True
            }),
            'visit_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'visit_time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'meeting_agenda': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'What is the purpose of this visit?',
                'rows': 3
            }),
            'meeting_outcome': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Describe the meeting outcome and key discussion points',
                'rows': 4
            }),
            'outcome_type': forms.Select(attrs={'class': 'form-input'}),
            'next_follow_up_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'location': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Meeting location/address'
            }),
            'gps_latitude': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'GPS Latitude',
                'step': '0.000001'
            }),
            'gps_longitude': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'GPS Longitude',
                'step': '0.000001'
            }),
            'visiting_card': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-input',
                'accept': 'image/*'
            }),
            'document': forms.FileInput(attrs={
                'class': 'form-input'
            }),
        }


class VisitApprovalForm(forms.ModelForm):
    """Form for approving/rejecting visit logs"""
    
    class Meta:
        model = VisitLog
        fields = ['approval_status']
        widgets = {
            'approval_status': forms.Select(attrs={'class': 'form-input'})
        }


class LeadForm(forms.ModelForm):
    """Form for creating and updating leads"""
    
    class Meta:
        model = Lead
        fields = [
            'lead_source', 'prospect', 'contact_person', 'mobile', 'email',
            'requirement_description', 'assigned_to', 'status', 'progress_percentage',
            'expected_closure_date', 'next_action_date', 'next_action_notes',
            'originating_visit', 'estimated_value', 'priority', 'notes'
        ]
        widgets = {
            'lead_source': forms.Select(attrs={'class': 'form-input'}),
            'prospect': forms.Select(attrs={'class': 'form-input', 'required': True}),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Primary contact person name'
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '+91 XXXXXXXXXX'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'email@example.com'
            }),
            'requirement_description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Describe the customer requirement in detail',
                'rows': 4
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-input'}),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'progress_percentage': forms.NumberInput(attrs={
                'class': 'form-input',
                'min': 0,
                'max': 100,
                'step': 5
            }),
            'expected_closure_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'next_action_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'next_action_notes': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Notes for the next action',
                'rows': 3
            }),
            'originating_visit': forms.Select(attrs={'class': 'form-input'}),
            'estimated_value': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Estimated deal value',
                'step': '0.01'
            }),
            'priority': forms.Select(attrs={'class': 'form-input'}),
            'notes': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Additional notes',
                'rows': 3
            }),
        }


class LeadActivityForm(forms.ModelForm):
    """Form for creating and updating lead activities/follow-ups"""
    
    class Meta:
        model = LeadActivity
        fields = [
            'lead', 'activity_type', 'activity_date', 'activity_time',
            'discussion_summary', 'outcome', 'remarks',
            'next_followup_date', 'next_followup_time', 'next_action_required',
            'status', 'lead_status_update',
            'attachment1', 'attachment2', 'attachment3',
            'contact_person', 'contact_number', 'contact_email'
        ]
        widgets = {
            'lead': forms.Select(attrs={
                'class': 'form-input',
                'required': True
            }),
            'activity_type': forms.Select(attrs={
                'class': 'form-input',
                'required': True
            }),
            'activity_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'activity_time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'discussion_summary': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Summary of discussion and key points covered',
                'rows': 4,
                'required': True
            }),
            'outcome': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Outcome of this activity',
                'rows': 3
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Additional remarks or notes',
                'rows': 3
            }),
            'next_followup_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'next_followup_time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'next_action_required': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'What needs to be done in the next follow-up?',
                'rows': 2
            }),
            'status': forms.Select(attrs={'class': 'form-input'}),
            'lead_status_update': forms.Select(attrs={
                'class': 'form-input',
                'help_text': 'Update lead status if changed'
            }),
            'attachment1': forms.FileInput(attrs={
                'class': 'form-input',
                'help_text': 'Proposal, quote, or document'
            }),
            'attachment2': forms.FileInput(attrs={
                'class': 'form-input',
                'help_text': 'Email copy, screenshot, or additional file'
            }),
            'attachment3': forms.FileInput(attrs={
                'class': 'form-input'
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Person contacted'
            }),
            'contact_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Contact number'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'contact@example.com'
            }),
        }


class QuotationForm(forms.ModelForm):
    """Form for creating and updating quotations"""
    
    class Meta:
        model = Quotation
        fields = [
            'prospect', 'contact_person', 'contact_email', 'contact_phone',
            'quote_date', 'valid_till', 'assigned_to',
            'currency', 'exchange_rate',
            'payment_terms_master', 'payment_terms', 
            'delivery_terms_master', 'delivery_terms',
            'reference_lead', 'reference_visit', 'reference_number',
            'customer_remarks', 'internal_notes',
            'discount_percentage', 'freight_charges'
        ]
        widgets = {
            'prospect': forms.Select(attrs={
                'class': 'form-input',
                'required': True
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Contact person name'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'contact@example.com'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Contact number'
            }),
            'quote_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'valid_till': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-input'}),
            'currency': forms.Select(attrs={'class': 'form-input'}),
            'exchange_rate': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.0001'
            }),
            'payment_terms_master': forms.Select(attrs={
                'class': 'form-input',
                'onchange': 'loadPaymentTerms(this)'
            }),
            'payment_terms': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Payment terms and conditions (auto-filled from master or enter custom)',
                'rows': 3
            }),
            'delivery_terms_master': forms.Select(attrs={
                'class': 'form-input',
                'onchange': 'loadDeliveryTerms(this)'
            }),
            'delivery_terms': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Delivery terms and conditions (auto-filled from master or enter custom)',
                'rows': 3
            }),
            'reference_lead': forms.Select(attrs={'class': 'form-input'}),
            'reference_visit': forms.Select(attrs={'class': 'form-input'}),
            'reference_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'PO, RFQ, or other reference'
            }),
            'customer_remarks': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Remarks visible to customer',
                'rows': 3
            }),
            'internal_notes': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Internal notes (not visible to customer)',
                'rows': 3
            }),
            'discount_percentage': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'freight_charges': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01'
            }),
        }


class QuotationItemForm(forms.ModelForm):
    """Form for quotation line items"""
    
    class Meta:
        model = QuotationItem
        fields = [
            'item_code', 'description', 'quantity', 'uom', 'unit_price',
            'discount_percentage', 'tax_percentage', 'remarks'
        ]
        widgets = {
            'item_code': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Item code'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Item description',
                'rows': 2
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0.01'
            }),
            'uom': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nos, Kg, Mtr, etc.'
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0'
            }),
            'discount_percentage': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'tax_percentage': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Additional remarks',
                'rows': 1
            }),
        }


# Formset for managing multiple quotation items
QuotationItemFormSet = inlineformset_factory(
    Quotation,
    QuotationItem,
    form=QuotationItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)


class QuotationAttachmentForm(forms.ModelForm):
    """Form for quotation attachments"""
    
    class Meta:
        model = QuotationAttachment
        fields = ['attachment_type', 'file', 'description']
        widgets = {
            'attachment_type': forms.Select(attrs={'class': 'form-input'}),
            'file': forms.FileInput(attrs={'class': 'form-input'}),
            'description': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Brief description of the file'
            }),
        }


class QuotationActivityForm(forms.ModelForm):
    """Form for adding comments/activities"""
    
    class Meta:
        model = QuotationActivity
        fields = ['activity_type', 'description', 'is_internal']
        widgets = {
            'activity_type': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Add a comment or note',
                'rows': 3
            }),
            'is_internal': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


class SalesOrderForm(forms.ModelForm):
    """Form for creating and updating sales orders"""
    
    class Meta:
        model = SalesOrder
        fields = [
            'prospect', 'contact_person', 'contact_email', 'contact_phone',
            'order_date', 'valid_till', 'assigned_to',
            'currency', 'exchange_rate',
            'payment_terms_master', 'payment_terms',
            'delivery_terms_master', 'delivery_terms',
            'reference_lead', 'reference_visit', 'reference_quotation', 'reference_number',
            'customer_remarks', 'internal_notes',
            'discount_percentage', 'freight_charges'
        ]
        widgets = {
            'prospect': forms.Select(attrs={
                'class': 'form-input',
                'required': True
            }),
            'contact_person': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Contact person name'
            }),
            'contact_email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'contact@example.com'
            }),
            'contact_phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Contact number'
            }),
            'order_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'valid_till': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'assigned_to': forms.Select(attrs={'class': 'form-input'}),
            'currency': forms.Select(attrs={'class': 'form-input'}),
            'exchange_rate': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.0001'
            }),
            'payment_terms_master': forms.Select(attrs={
                'class': 'form-input',
                'onchange': 'loadPaymentTerms(this)'
            }),
            'payment_terms': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Payment terms and conditions (auto-filled from master or enter custom)',
                'rows': 3
            }),
            'delivery_terms_master': forms.Select(attrs={
                'class': 'form-input',
                'onchange': 'loadDeliveryTerms(this)'
            }),
            'delivery_terms': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Delivery terms and conditions (auto-filled from master or enter custom)',
                'rows': 3
            }),
            'reference_lead': forms.Select(attrs={'class': 'form-input'}),
            'reference_visit': forms.Select(attrs={'class': 'form-input'}),
            'reference_quotation': forms.Select(attrs={'class': 'form-input'}),
            'reference_number': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'PO, RFQ, or other reference'
            }),
            'customer_remarks': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Remarks visible to customer',
                'rows': 3
            }),
            'internal_notes': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Internal notes (not visible to customer)',
                'rows': 3
            }),
            'discount_percentage': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'freight_charges': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01'
            }),
        }


class SalesOrderItemForm(forms.ModelForm):
    """Form for sales order line items"""
    
    class Meta:
        model = SalesOrderItem
        fields = [
            'item_code', 'description', 'quantity', 'uom', 'unit_price',
            'discount_percentage', 'tax_percentage', 'remarks'
        ]
        widgets = {
            'item_code': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Item code'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Item description',
                'rows': 2
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0.01'
            }),
            'uom': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Nos, Kg, Mtr, etc.'
            }),
            'unit_price': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0'
            }),
            'discount_percentage': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'tax_percentage': forms.NumberInput(attrs={
                'class': 'form-input',
                'step': '0.01',
                'min': '0',
                'max': '100'
            }),
            'remarks': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Additional remarks',
                'rows': 1
            }),
        }


# Formset for managing multiple sales order items
SalesOrderItemFormSet = inlineformset_factory(
    SalesOrder,
    SalesOrderItem,
    form=SalesOrderItemForm,
    extra=1,
    can_delete=True,
    min_num=1,
    validate_min=True
)


class SalesOrderAttachmentForm(forms.ModelForm):
    """Form for sales order attachments"""
    
    class Meta:
        model = SalesOrderAttachment
        fields = ['attachment_type', 'file', 'description']
        widgets = {
            'attachment_type': forms.Select(attrs={'class': 'form-input'}),
            'file': forms.FileInput(attrs={'class': 'form-input'}),
            'description': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Brief description of the file'
            }),
        }


class SalesOrderActivityForm(forms.ModelForm):
    """Form for adding comments/activities"""
    
    class Meta:
        model = SalesOrderActivity
        fields = ['activity_type', 'description', 'is_internal']
        widgets = {
            'activity_type': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Add a comment or note',
                'rows': 3
            }),
            'is_internal': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


# ==========================
# Service Call Forms
# ==========================

class ServiceCallForm(forms.ModelForm):
    """
    Form for creating and updating service calls
    """

    STATUS_UI_CHOICES = [
        ('NEW', 'Open'),
        ('CLOSED', 'Closed'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_UI_CHOICES,
        widget=forms.Select(attrs={'class': 'form-input'})
    )

    reopen_reason = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'rows': 3,
            'placeholder': 'Reason for reopening the service call'
        })
    )

    class Meta:
        model = ServiceCall
        fields = [
            'service_type',
            'priority',
            'customer',
            'contact_person',
            'contact_phone',
            'contact_email',
            'preferred_visit_date',
            'assigned_technician',
            'assigned_team',
            'mode',
            'fault_category',
            'symptom',
            'problem_type',
            'parts_required',
            'warranty_status',
            'estimated_cost',
            'billable',
            'status',
            'item_name',
            'serial_number',
            'origin',
            'call_type',
            'service_number',            
        ]

        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-input'}),
            'priority': forms.Select(attrs={'class': 'form-input'}),
            'customer': forms.Select(attrs={'class': 'form-input'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-input'}),
            'contact_email': forms.EmailInput(attrs={'class': 'form-input'}),
            'preferred_visit_date': forms.DateTimeInput(attrs={
                'class': 'form-input',
                'type': 'datetime-local'
            }),
            'assigned_technician': forms.Select(attrs={'class': 'form-input'}),
            'assigned_team': forms.TextInput(attrs={'class': 'form-input'}),
            'mode': forms.Select(attrs={'class': 'form-input'}),
            'fault_category': forms.TextInput(attrs={'class': 'form-input'}),
            'symptom': forms.TextInput(attrs={'class': 'form-input'}),
            'problem_description': forms.Textarea(attrs={'class': 'form-input','rows': 4}),
            'parts_required': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'warranty_status': forms.Select(attrs={'class': 'form-input'}),
            'estimated_cost': forms.NumberInput(attrs={'class': 'form-input'}),
            'billable': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'item_name': forms.TextInput(attrs={'class': 'form-input','placeholder': 'Equipment / Item name'
    }),
            'serial_number': forms.TextInput(attrs={'class': 'form-input','placeholder': 'Serial number'}),
            'origin': forms.Select(attrs={'class': 'form-input'}),
            'call_type': forms.Select(attrs={'class': 'form-input'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        if self.instance.pk:
            old_status = ServiceCall.objects.get(pk=self.instance.pk).status
            new_status = cleaned_data.get('status')

            if old_status == 'CLOSED' and new_status != 'CLOSED':
                if not cleaned_data.get('reopen_reason'):
                    raise forms.ValidationError(
                        "Reopen reason is required when reopening a closed service call."
                    )

        return cleaned_data
class ServiceCallItemForm(forms.ModelForm):
    """Form for service call items/parts"""

    class Meta:
        model = ServiceCallItem
        fields = [
            'item_master',
            'item_code',
            'product_serial_no',
            'description',
            'fault_found',
            'quantity',
            'uom',
            'item_type',
            'unit_cost',
            'unit_price',
            'labour_hours',
            'labour_rate',
            'tax_percentage',
            'warranty_covered',
            'batch_no',
            'serial_number',
            'remarks'
        ]

        widgets = {
            'item_master': forms.Select(attrs={'class': 'form-input'}),
            'item_code': forms.TextInput(attrs={'class': 'form-input'}),
            'product_serial_no': forms.TextInput(attrs={'class': 'form-input'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'fault_found': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input'}),
            'uom': forms.TextInput(attrs={'class': 'form-input'}),
            'item_type': forms.Select(attrs={'class': 'form-input'}),
            'unit_cost': forms.NumberInput(attrs={'class': 'form-input'}),
            'unit_price': forms.NumberInput(attrs={'class': 'form-input'}),
            'labour_hours': forms.NumberInput(attrs={'class': 'form-input'}),
            'labour_rate': forms.NumberInput(attrs={'class': 'form-input'}),
            'tax_percentage': forms.NumberInput(attrs={'class': 'form-input'}),
            'warranty_covered': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
            'batch_no': forms.TextInput(attrs={'class': 'form-input'}),
            'serial_number': forms.TextInput(attrs={'class': 'form-input'}),
            'remarks': forms.Textarea(attrs={'class': 'form-input', 'rows': 2}),
    }
class ServiceCallAttachmentForm(forms.ModelForm):
    """Form for service call attachments"""
    
    class Meta:
        model = ServiceCallAttachment
        fields = ['file', 'file_type', 'description']
        widgets = {
            'file': forms.FileInput(attrs={'class': 'form-input'}),
            'file_type': forms.Select(attrs={'class': 'form-input'}),
            'description': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Brief description of the file'
            }),
        }


class ServiceCallActivityForm(forms.ModelForm):
    """Form for service call activities"""
    
    class Meta:
        model = ServiceActivity
        fields = ['activity_type', 'activity_date', 'start_time', 'end_time', 'description', 'performed_by', 'remarks', 'is_billable']
        widgets = {
            'activity_type': forms.Select(attrs={'class': 'form-input'}),
            'activity_date': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-input',
                'type': 'time'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Activity description',
                'rows': 3
            }),
            'performed_by': forms.Select(attrs={'class': 'form-input'}),
            'remarks': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Additional remarks',
                'rows': 2
            }),
            'is_billable': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),
        }


# Formsets for service call items - configured for single item only
ServiceCallItemFormSet = inlineformset_factory(
    ServiceCall, ServiceCallItem, form=ServiceCallItemForm,
    extra=1, can_delete=False, min_num=0, validate_min=False
)
