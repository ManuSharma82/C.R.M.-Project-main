from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView, DeleteView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .forms import (CustomSignUpForm, CustomSignInForm, ProspectCustomerForm, VisitLogForm, 
                    VisitApprovalForm, LeadForm, LeadActivityForm, QuotationForm, QuotationItemFormSet,
                    QuotationAttachmentForm, QuotationActivityForm, SalesOrderForm, SalesOrderItemFormSet,
                    SalesOrderAttachmentForm, SalesOrderActivityForm, ServiceCallForm, ServiceCallItemFormSet,
                    ServiceCallAttachmentForm, ServiceCallActivityForm)
from .models import (ProspectCustomer, VisitLog, SalesEmployee, Lead, LeadHistory, LeadActivity,
                     Quotation, QuotationItem, QuotationAttachment, QuotationActivity,
                     SalesOrder, SalesOrderItem, SalesOrderAttachment, SalesOrderActivity,
                     ServiceCall, ServiceCallItem, ServiceCallAttachment, ServiceActivity)

# Create your views here.
class IndexView(TemplateView):
    template_name = 'newapp/index.html'


class SignUpView(CreateView):
    form_class = CustomSignUpForm
    template_name = 'newapp/signup.html'
    success_url = reverse_lazy('newapp:index')
    
    def form_valid(self, form):
        # Save the user and log them in automatically
        user = form.save()
        login(self.request, user)
        return redirect(self.success_url)


class SignInView(LoginView):
    form_class = CustomSignInForm
    template_name = 'newapp/signin.html'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('newapp:dashboard')


def logout_view(request):
    """Logout user and redirect to index page immediately"""
    logout(request)
    return redirect('newapp:index')


# CRM Dashboard
class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'newapp/dashboard.html'
    login_url = 'newapp:signin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get effective user (admin viewing as another user or current user)
        view_as_user_id = self.request.GET.get('view_as_user')
        if view_as_user_id and view_as_user_id != 'self' and (self.request.user.is_staff or self.request.user.is_superuser):
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(id=view_as_user_id)
                context['viewing_as'] = user.get_full_name() or user.username
            except (ValueError, User.DoesNotExist):
                user = self.request.user
        else:
            user = self.request.user
        
        # Date calculations
        today = timezone.now().date()
        month_start = today.replace(day=1)
        week_ago = today - timedelta(days=7)
        
        # Check if admin (and not viewing as specific user)
        is_admin_view = (self.request.user.is_staff or self.request.user.is_superuser) and (not view_as_user_id or view_as_user_id == 'self')
        context['is_admin'] = is_admin_view
        
        # Prepare dashboard data for JavaScript
        dashboard_data = {}
        
        if is_admin_view:
            # ADMIN DASHBOARD - Aggregate data across all users
            
            # Total Visits (Today / Month)
            visits_today = VisitLog.objects.filter(visit_date=today).count()
            visits_month = VisitLog.objects.filter(visit_date__gte=month_start).count()
            
            # Total Leads (By Stage)
            leads_by_stage = list(ProspectCustomer.objects.values('status').annotate(count=Count('id')).order_by('status'))
            total_leads = ProspectCustomer.objects.count()
            context['visits_today'] = visits_today
            context['visits_month'] = visits_month
            context['total_visits'] = VisitLog.objects.count()
            
            # Total Leads (By Stage)
            context['leads_by_stage'] = ProspectCustomer.objects.values('status').annotate(count=Count('id')).order_by('status')
            context['total_leads'] = total_leads
            context['active_leads'] = ProspectCustomer.objects.filter(status__in=['NEW', 'CONTACTED', 'QUALIFIED', 'PROPOSAL', 'NEGOTIATION']).count()
            
            # Conversion %
            total_prospects = ProspectCustomer.objects.count()
            converted_prospects = ProspectCustomer.objects.filter(status='WON').count()
            conversion_rate = round((converted_prospects / total_prospects * 100), 1) if total_prospects > 0 else 0
            
            # Upcoming follow-ups
            upcoming_followups_raw = VisitLog.objects.filter(
                next_follow_up_date__gte=today,
                next_follow_up_date__lte=today + timedelta(days=7)
            ).select_related('prospect', 'sales_employee__user').values(
                'prospect__name', 'prospect__company_name', 'next_follow_up_date', 
                'visit_date', 'sales_employee__user__first_name', 'sales_employee__user__last_name'
            )
            
            # Convert date objects to strings for JSON serialization
            upcoming_followups = []
            for followup in upcoming_followups_raw:
                upcoming_followups.append({
                    'prospect__name': followup['prospect__name'],
                    'prospect__company_name': followup['prospect__company_name'],
                    'next_follow_up_date': followup['next_follow_up_date'].strftime('%Y-%m-%d') if followup['next_follow_up_date'] else None,
                    'visit_date': followup['visit_date'].strftime('%Y-%m-%d') if followup['visit_date'] else None,
                    'sales_employee__user__first_name': followup['sales_employee__user__first_name'] or '',
                    'sales_employee__user__last_name': followup['sales_employee__user__last_name'] or ''
                })
            
            dashboard_data = {
                'visits_today': visits_today,
                'visits_month': visits_month,
                'total_leads': total_leads,
                'conversion_rate': conversion_rate,
                'converted_count': converted_prospects,
                'leads_by_stage': leads_by_stage,
                'upcoming_followups': upcoming_followups
            }
            
            # Set context variables for template rendering
            context['visits_today'] = visits_today
            context['visits_month'] = visits_month
            context['total_visits'] = VisitLog.objects.count()
            context['leads_by_stage'] = leads_by_stage
            context['total_leads'] = total_leads
            context['active_leads'] = ProspectCustomer.objects.filter(status__in=['NEW', 'CONTACTED', 'QUALIFIED', 'PROPOSAL', 'NEGOTIATION']).count()
            context['conversion_rate'] = conversion_rate
            context['converted_count'] = converted_prospects
            
            # Employee-wise performance
            context['employee_performance'] = SalesEmployee.objects.annotate(
                visit_count=Count('visits'),
                pending_visits=Count('visits', filter=Q(visits__approval_status='PENDING')),
                completed_visits=Count('visits', filter=Q(visits__status='COMPLETED'))
            ).select_related('user').order_by('-visit_count')[:10]
            
            # Upcoming Follow-ups (All employees)
            context['upcoming_followups'] = VisitLog.objects.filter(
                next_follow_up_date__gte=today,
                next_follow_up_date__lte=today + timedelta(days=7)
            ).select_related('prospect', 'sales_employee__user').order_by('next_follow_up_date')[:10]
            
            # Pending Approvals
            context['pending_approvals'] = VisitLog.objects.filter(approval_status='PENDING').count()
            
            context['is_sales_employee'] = True
            
        else:
            # SALES EXECUTIVE/REP DASHBOARD - Individual data
            try:
                sales_employee = user.sales_profile
                
                # Today's Visits
                context['visits_today'] = VisitLog.objects.filter(
                    sales_employee=sales_employee,
                    visit_date=today
                ).count()
                
                # Monthly Visit Count
                visits_month = VisitLog.objects.filter(
                    sales_employee=sales_employee,
                    visit_date__gte=month_start
                ).count()
                context['visits_month'] = visits_month
                context['total_visits'] = VisitLog.objects.filter(sales_employee=sales_employee).count()
                
                # Pending Follow-ups
                upcoming_followups_raw = VisitLog.objects.filter(
                    sales_employee=sales_employee,
                    next_follow_up_date__gte=today,
                    next_follow_up_date__lte=today + timedelta(days=7)
                ).select_related('prospect').values(
                    'prospect__name', 'prospect__company_name', 'next_follow_up_date', 'visit_date',
                    'sales_employee__user__first_name', 'sales_employee__user__last_name'
                )
                
                # Convert date objects to strings for JSON serialization
                upcoming_followups = []
                for followup in upcoming_followups_raw:
                    upcoming_followups.append({
                        'prospect__name': followup['prospect__name'],
                        'prospect__company_name': followup['prospect__company_name'],
                        'next_follow_up_date': followup['next_follow_up_date'].strftime('%Y-%m-%d') if followup['next_follow_up_date'] else None,
                        'visit_date': followup['visit_date'].strftime('%Y-%m-%d') if followup['visit_date'] else None,
                        'sales_employee__user__first_name': followup['sales_employee__user__first_name'] or '',
                        'sales_employee__user__last_name': followup['sales_employee__user__last_name'] or ''
                    })
                
                # Active Leads
                active_leads = ProspectCustomer.objects.filter(
                    assigned_to=sales_employee,
                    status__in=['NEW', 'CONTACTED', 'QUALIFIED', 'PROPOSAL', 'NEGOTIATION']
                ).count()
                total_leads = ProspectCustomer.objects.filter(assigned_to=sales_employee).count()
                
                # Conversion Status
                my_prospects = total_leads
                my_converted = ProspectCustomer.objects.filter(assigned_to=sales_employee, status='WON').count()
                conversion_rate = round((my_converted / my_prospects * 100), 1) if my_prospects > 0 else 0
                
                # Leads by Stage
                leads_by_stage = list(ProspectCustomer.objects.filter(assigned_to=sales_employee).values('status').annotate(count=Count('id')).order_by('status'))
                
                dashboard_data = {
                    'visits_today': visits_today,
                    'visits_month': visits_month,
                    'total_leads': total_leads,
                    'active_leads': active_leads,
                    'conversion_rate': conversion_rate,
                    'converted_count': my_converted,
                    'leads_by_stage': leads_by_stage,
                    'upcoming_followups': upcoming_followups
                }
                
                # Set context variables for template rendering
                context['visits_today'] = visits_today
                context['visits_month'] = visits_month
                context['total_visits'] = VisitLog.objects.filter(sales_employee=sales_employee).count()
                context['upcoming_followups'] = VisitLog.objects.filter(
                    sales_employee=sales_employee,
                    next_follow_up_date__gte=today,
                    next_follow_up_date__lte=today + timedelta(days=7)
                ).select_related('prospect').order_by('next_follow_up_date')[:10]
                context['pending_followups_count'] = context['upcoming_followups'].count()
                context['active_leads'] = active_leads
                context['total_leads'] = total_leads
                context['conversion_rate'] = conversion_rate
                context['converted_count'] = my_converted
                context['leads_by_stage'] = leads_by_stage
                
                # Pending Approvals (own)
                context['pending_approvals'] = VisitLog.objects.filter(
                    sales_employee=sales_employee,
                    approval_status='PENDING'
                ).count()
                
                # Recent visits
                context['recent_visits'] = VisitLog.objects.filter(
                    sales_employee=sales_employee
                ).select_related('prospect').order_by('-visit_date', '-visit_time')[:5]
                
                context['is_sales_employee'] = True
                context['sales_employee'] = sales_employee
                
            except SalesEmployee.DoesNotExist:
                context['is_sales_employee'] = False
                context['visits_today'] = 0
                context['visits_month'] = 0
                context['total_visits'] = 0
                context['pending_followups_count'] = 0
                context['active_leads'] = 0
                context['total_leads'] = 0
                context['conversion_rate'] = 0
                context['converted_count'] = 0
                context['pending_approvals'] = 0
                context['recent_visits'] = []
                context['upcoming_followups'] = []
                context['leads_by_stage'] = []
                
                dashboard_data = {
                    'visits_today': 0,
                    'visits_month': 0,
                    'total_leads': 0,
                    'conversion_rate': 0,
                    'converted_count': 0,
                    'leads_by_stage': [],
                    'upcoming_followups': []
                }
        
        # Convert dashboard data to JSON for JavaScript
        import json
        context['dashboard_json'] = json.dumps(dashboard_data)
        
        return context


# Prospect Management Views
class ProspectListView(LoginRequiredMixin, ListView):
    model = ProspectCustomer
    template_name = 'newapp/prospect_list.html'
    context_object_name = 'prospects'
    paginate_by = 20
    login_url = 'newapp:signin'
    
    def get_queryset(self):
        queryset = ProspectCustomer.objects.all().select_related('assigned_to__user')
        
        # Filter by search query
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(company_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(email__icontains=search)
            )
        
        # Filter by type
        prospect_type = self.request.GET.get('type')
        if prospect_type:
            queryset = queryset.filter(type=prospect_type)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')


class ProspectCreateView(LoginRequiredMixin, CreateView):
    model = ProspectCustomer
    form_class = ProspectCustomerForm
    template_name = 'newapp/prospect_form.html'
    success_url = reverse_lazy('newapp:prospect_list')
    login_url = 'newapp:signin'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class ProspectUpdateView(LoginRequiredMixin, UpdateView):
    model = ProspectCustomer
    form_class = ProspectCustomerForm
    template_name = 'newapp/prospect_form.html'
    success_url = reverse_lazy('newapp:prospect_list')
    login_url = 'newapp:signin'


class ProspectDetailView(LoginRequiredMixin, DetailView):
    model = ProspectCustomer
    template_name = 'newapp/prospect_detail.html'
    context_object_name = 'prospect'
    login_url = 'newapp:signin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['visits'] = VisitLog.objects.filter(
            prospect=self.object
        ).select_related('sales_employee__user').order_by('-visit_date', '-visit_time')
        return context


# Visit Management Views
class VisitListView(LoginRequiredMixin, ListView):
    model = VisitLog
    template_name = 'newapp/visit_list.html'
    context_object_name = 'visits'
    paginate_by = 20
    login_url = 'newapp:signin'
    
    def get_queryset(self):
        user = self.request.user
        
        try:
            sales_employee = user.sales_profile
            queryset = VisitLog.objects.filter(
                sales_employee=sales_employee
            ).select_related('prospect', 'sales_employee__user')
        except SalesEmployee.DoesNotExist:
            queryset = VisitLog.objects.none()
        
        # Filter by date range
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(visit_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(visit_date__lte=end_date)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by approval status
        approval_status = self.request.GET.get('approval_status')
        if approval_status:
            queryset = queryset.filter(approval_status=approval_status)
        
        return queryset.order_by('-visit_date', '-visit_time')


class VisitCreateView(LoginRequiredMixin, CreateView):
    model = VisitLog
    form_class = VisitLogForm
    template_name = 'newapp/visit_form.html'
    success_url = reverse_lazy('newapp:visit_list')
    login_url = 'newapp:signin'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Set initial values for date and time
        if not form.instance.pk:
            form.initial['visit_date'] = timezone.now().date()
            form.initial['visit_time'] = timezone.now().time()
        return form
    
    def form_valid(self, form):
        try:
            sales_employee = self.request.user.sales_profile
            form.instance.sales_employee = sales_employee
            return super().form_valid(form)
        except SalesEmployee.DoesNotExist:
            form.add_error(None, "You must be registered as a sales employee to create visits.")
            return self.form_invalid(form)


class VisitUpdateView(LoginRequiredMixin, UpdateView):
    model = VisitLog
    form_class = VisitLogForm
    template_name = 'newapp/visit_form.html'
    success_url = reverse_lazy('newapp:visit_list')
    login_url = 'newapp:signin'
    
    def get_queryset(self):
        # Only allow users to edit their own visits
        try:
            sales_employee = self.request.user.sales_profile
            return VisitLog.objects.filter(sales_employee=sales_employee)
        except SalesEmployee.DoesNotExist:
            return VisitLog.objects.none()


class VisitDetailView(LoginRequiredMixin, DetailView):
    model = VisitLog
    template_name = 'newapp/visit_detail.html'
    context_object_name = 'visit'
    login_url = 'newapp:signin'


@login_required(login_url='newapp:signin')
def approve_visit(request, pk):
    """Approve or reject visit logs (for Sales Heads/Admins)"""
    visit = get_object_or_404(VisitLog, pk=pk)
    
    # Check if user has permission to approve
    try:
        sales_employee = request.user.sales_profile
        if sales_employee.role not in ['SALES_HEAD', 'MANAGER', 'ADMIN']:
            return JsonResponse({'error': 'You do not have permission to approve visits'}, status=403)
    except SalesEmployee.DoesNotExist:
        return JsonResponse({'error': 'Sales employee profile not found'}, status=403)
    
    if request.method == 'POST':
        approval_status = request.POST.get('approval_status')
        if approval_status in ['APPROVED', 'REJECTED']:
            visit.approval_status = approval_status
            visit.approved_by = request.user
            visit.approved_at = timezone.now()
            visit.save()
            return redirect('newapp:visit_detail', pk=pk)
    
    return redirect('newapp:visit_detail', pk=pk)


# Single Page Visit Management
class VisitManagementView(LoginRequiredMixin, TemplateView):
    template_name = 'newapp/visit_management.html'
    login_url = 'newapp:signin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get effective user (admin viewing as another user or current user)
        view_as_user_id = self.request.GET.get('view_as_user')
        if view_as_user_id and view_as_user_id != 'self' and (self.request.user.is_staff or self.request.user.is_superuser):
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(id=view_as_user_id)
                context['viewing_as'] = user.get_full_name() or user.username
            except (ValueError, User.DoesNotExist):
                user = self.request.user
        else:
            user = self.request.user
        
        try:
            sales_employee = user.sales_profile
            today = timezone.now().date()
            week_ago = today - timedelta(days=7)
            
            # My visits
            context['my_visits'] = VisitLog.objects.filter(
                sales_employee=sales_employee
            ).select_related('prospect', 'sales_employee__user').order_by('-visit_date', '-visit_time')[:20]
            
            # Statistics
            context['todays_visits'] = VisitLog.objects.filter(
                sales_employee=sales_employee,
                visit_date=today
            ).count()
            
            context['week_visits'] = VisitLog.objects.filter(
                sales_employee=sales_employee,
                visit_date__gte=week_ago
            ).count()
            
            context['pending_visits'] = VisitLog.objects.filter(
                sales_employee=sales_employee,
                approval_status='PENDING'
            ).count()
            
            context['total_visits'] = VisitLog.objects.filter(
                sales_employee=sales_employee
            ).count()
            
            # Check if user is approver
            context['is_approver'] = sales_employee.role in ['ADMIN', 'MANAGER', 'SALES_HEAD']
            
            # Pending approval visits (if approver)
            if context['is_approver']:
                context['pending_approval_visits'] = VisitLog.objects.filter(
                    approval_status='PENDING'
                ).select_related('prospect', 'sales_employee__user').order_by('-visit_date', '-visit_time')[:20]
            else:
                context['pending_approval_visits'] = []
            
            # All visits (limited view)
            context['all_visits'] = VisitLog.objects.all().select_related(
                'prospect', 'sales_employee__user'
            ).order_by('-visit_date', '-visit_time')[:50]
            
            # Report stats
            all_visits_query = VisitLog.objects.all()
            context['completed_visits'] = all_visits_query.filter(status='COMPLETED').count()
            context['approved_visits'] = all_visits_query.filter(approval_status='APPROVED').count()
            
            # Prospects for dropdown
            context['prospects'] = ProspectCustomer.objects.all().order_by('name')[:100]
            
            # Current date/time for form
            context['today'] = today
            context['current_time'] = timezone.now().time().strftime('%H:%M')
            
        except SalesEmployee.DoesNotExist:
            context['my_visits'] = []
            context['is_approver'] = False
            context['pending_approval_visits'] = []
            context['all_visits'] = []
            context['todays_visits'] = 0
            context['week_visits'] = 0
            context['pending_visits'] = 0
            context['total_visits'] = 0
            context['completed_visits'] = 0
            context['approved_visits'] = 0
            context['prospects'] = []
            context['today'] = timezone.now().date()
            context['current_time'] = timezone.now().time().strftime('%H:%M')
        
        return context


# Reports
class VisitReportView(LoginRequiredMixin, TemplateView):
    template_name = 'newapp/visit_report.html'
    login_url = 'newapp:signin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get effective user for filtering (admin viewing as another user or current user)
        view_as_user_id = self.request.GET.get('view_as_user')
        filter_user = None
        if view_as_user_id and view_as_user_id != 'self' and (self.request.user.is_staff or self.request.user.is_superuser):
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                filter_user = User.objects.get(id=view_as_user_id)
                context['viewing_as'] = filter_user.get_full_name() or filter_user.username
            except (ValueError, User.DoesNotExist):
                pass
        
        # Date filters
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        
        # Base queryset
        visits = VisitLog.objects.all().select_related('sales_employee__user', 'prospect')
        
        # Filter by user if viewing as specific user
        if filter_user:
            try:
                sales_employee = filter_user.sales_profile
                visits = visits.filter(sales_employee=sales_employee)
            except:
                pass
        
        if start_date:
            visits = visits.filter(visit_date__gte=start_date)
            context['start_date'] = start_date
        if end_date:
            visits = visits.filter(visit_date__lte=end_date)
            context['end_date'] = end_date
        
        # Statistics
        context['total_visits'] = visits.count()
        context['completed_visits'] = visits.filter(status='COMPLETED').count()
        context['pending_approvals'] = visits.filter(approval_status='PENDING').count()
        context['approved_visits'] = visits.filter(approval_status='APPROVED').count()
        
        # Outcome breakdown
        context['outcome_stats'] = visits.values('outcome_type').annotate(count=Count('id'))
        
        # Region-wise breakdown (if available)
        context['region_stats'] = visits.values(
            'sales_employee__region'
        ).annotate(count=Count('id')).order_by('-count')
        
        # Top performers
        context['top_performers'] = visits.values(
            'sales_employee__user__username',
            'sales_employee__employee_id'
        ).annotate(visit_count=Count('id')).order_by('-visit_count')[:10]
        
        context['visits'] = visits.order_by('-visit_date', '-visit_time')[:50]
        
        return context


# Lead Management Views
class LeadListView(LoginRequiredMixin, ListView):
    model = Lead
    template_name = 'newapp/lead_list.html'
    context_object_name = 'leads'
    paginate_by = 20
    login_url = 'newapp:signin'
    
    def get_queryset(self):
        user = self.request.user
        
        # Check if viewing as another user (admin feature)
        view_as_user_id = self.request.GET.get('view_as_user')
        if view_as_user_id and view_as_user_id != 'self' and (user.is_staff or user.is_superuser):
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                user = User.objects.get(id=view_as_user_id)
            except:
                pass
        
        # Admin sees all leads, sales reps see only their assigned leads
        if user.is_staff or user.is_superuser:
            queryset = Lead.objects.all()
        else:
            try:
                sales_employee = user.sales_profile
                queryset = Lead.objects.filter(assigned_to=sales_employee)
            except SalesEmployee.DoesNotExist:
                queryset = Lead.objects.none()
        
        queryset = queryset.select_related('prospect', 'assigned_to__user', 'originating_visit')
        
        # Filter by search query
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(lead_id__icontains=search) |
                Q(prospect__name__icontains=search) |
                Q(prospect__company_name__icontains=search) |
                Q(contact_person__icontains=search) |
                Q(mobile__icontains=search) |
                Q(email__icontains=search) |
                Q(requirement_description__icontains=search)
            )
        
        # Filter by source
        lead_source = self.request.GET.get('source')
        if lead_source:
            queryset = queryset.filter(lead_source=lead_source)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by priority
        priority = self.request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter by assigned employee
        assigned_to = self.request.GET.get('assigned_to')
        if assigned_to:
            queryset = queryset.filter(assigned_to__id=assigned_to)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add today's date for comparisons
        context['today'] = timezone.now().date()
        
        # Add filter options
        context['lead_sources'] = Lead.SOURCE_CHOICES
        context['lead_statuses'] = Lead.STATUS_CHOICES
        context['priorities'] = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High'), ('URGENT', 'Urgent')]
        context['sales_employees'] = SalesEmployee.objects.filter(is_active=True).select_related('user')
        
        # Preserve filter values
        context['current_source'] = self.request.GET.get('source', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_priority'] = self.request.GET.get('priority', '')
        context['current_assigned'] = self.request.GET.get('assigned_to', '')
        context['search_query'] = self.request.GET.get('search', '')
        
        return context


class LeadCreateView(LoginRequiredMixin, CreateView):
    model = Lead
    form_class = LeadForm
    template_name = 'newapp/lead_form.html'
    success_url = reverse_lazy('newapp:lead_list')
    login_url = 'newapp:signin'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Pre-fill from visit if coming from visit detail page
        visit_id = self.request.GET.get('from_visit')
        if visit_id:
            try:
                visit = VisitLog.objects.get(pk=visit_id)
                form.initial['lead_source'] = 'VISIT'
                form.initial['prospect'] = visit.prospect
                form.initial['contact_person'] = visit.prospect.name
                form.initial['mobile'] = visit.prospect.phone
                form.initial['email'] = visit.prospect.email
                form.initial['assigned_to'] = visit.sales_employee
                form.initial['originating_visit'] = visit
                if visit.meeting_outcome:
                    form.initial['requirement_description'] = visit.meeting_outcome
            except VisitLog.DoesNotExist:
                pass
        
        # Auto-assign to current user if they are a sales employee
        if not form.initial.get('assigned_to'):
            try:
                sales_employee = self.request.user.sales_profile
                form.initial['assigned_to'] = sales_employee
            except SalesEmployee.DoesNotExist:
                pass
        
        return form
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Log creation in history
        LeadHistory.objects.create(
            lead=self.object,
            changed_by=self.request.user,
            field_name='created',
            new_value='Lead created',
            notes=f'Lead created from {self.object.lead_source}'
        )
        
        return response


class LeadUpdateView(LoginRequiredMixin, UpdateView):
    model = Lead
    form_class = LeadForm
    template_name = 'newapp/lead_form.html'
    success_url = reverse_lazy('newapp:lead_list')
    login_url = 'newapp:signin'
    
    def get_queryset(self):
        user = self.request.user
        # Admin can edit all leads, sales reps can only edit their assigned leads
        if user.is_staff or user.is_superuser:
            return Lead.objects.all()
        else:
            try:
                sales_employee = user.sales_profile
                return Lead.objects.filter(assigned_to=sales_employee)
            except SalesEmployee.DoesNotExist:
                return Lead.objects.none()
    
    def form_valid(self, form):
        # Track what changed
        if form.has_changed():
            for field in form.changed_data:
                old_value = getattr(form.instance, field, None)
                new_value = form.cleaned_data.get(field)
                
                # Convert to string for storage
                old_val_str = str(old_value) if old_value else ''
                new_val_str = str(new_value) if new_value else ''
                
                LeadHistory.objects.create(
                    lead=self.object,
                    changed_by=self.request.user,
                    field_name=field,
                    old_value=old_val_str,
                    new_value=new_val_str
                )
        
        return super().form_valid(form)


class LeadDetailView(LoginRequiredMixin, DetailView):
    model = Lead
    template_name = 'newapp/lead_detail.html'
    context_object_name = 'lead'
    login_url = 'newapp:signin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get lead history
        context['history'] = LeadHistory.objects.filter(
            lead=self.object
        ).select_related('changed_by').order_by('-changed_at')
        
        # Get related visits
        context['visits'] = VisitLog.objects.filter(
            prospect=self.object.prospect
        ).select_related('sales_employee__user').order_by('-visit_date', '-visit_time')[:10]
        
        # Get activities for this lead
        context['activities'] = LeadActivity.objects.filter(
            lead=self.object
        ).select_related('created_by').order_by('-activity_date', '-activity_time')
        
        return context


# Lead Activity Management Views
class ActivityListView(LoginRequiredMixin, ListView):
    model = LeadActivity
    template_name = 'newapp/activity_list.html'
    context_object_name = 'activities'
    paginate_by = 20
    login_url = 'newapp:signin'
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin sees all activities, sales reps see only their leads' activities
        if user.is_staff or user.is_superuser:
            queryset = LeadActivity.objects.all()
        else:
            try:
                sales_employee = user.sales_profile
                queryset = LeadActivity.objects.filter(lead__assigned_to=sales_employee)
            except SalesEmployee.DoesNotExist:
                queryset = LeadActivity.objects.none()
        
        queryset = queryset.select_related('lead', 'lead__prospect', 'lead__assigned_to__user', 'created_by')
        
        # Filter by lead
        lead_id = self.request.GET.get('lead')
        if lead_id:
            queryset = queryset.filter(lead__id=lead_id)
        
        # Filter by activity type
        activity_type = self.request.GET.get('activity_type')
        if activity_type:
            queryset = queryset.filter(activity_type=activity_type)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by date range
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(activity_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(activity_date__lte=end_date)
        
        return queryset.order_by('-activity_date', '-activity_time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add today's date
        context['today'] = timezone.now().date()
        
        # Add filter options
        context['activity_types'] = LeadActivity.ACTIVITY_TYPE_CHOICES
        context['activity_statuses'] = LeadActivity.STATUS_CHOICES
        
        # Preserve filter values
        context['current_lead'] = self.request.GET.get('lead', '')
        context['current_activity_type'] = self.request.GET.get('activity_type', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        
        return context


class ActivityCreateView(LoginRequiredMixin, CreateView):
    model = LeadActivity
    form_class = LeadActivityForm
    template_name = 'newapp/activity_form.html'
    success_url = reverse_lazy('newapp:activity_list')
    login_url = 'newapp:signin'
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        
        # Pre-fill lead if coming from lead detail page
        lead_id = self.request.GET.get('lead_id')
        if lead_id:
            try:
                lead = Lead.objects.get(pk=lead_id)
                form.initial['lead'] = lead
                form.initial['contact_person'] = lead.contact_person
                form.initial['contact_number'] = lead.mobile
                form.initial['contact_email'] = lead.email
            except Lead.DoesNotExist:
                pass
        
        # Set initial date and time
        if not form.instance.pk:
            form.initial['activity_date'] = timezone.now().date()
            form.initial['activity_time'] = timezone.now().time()
        
        return form
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        response = super().form_valid(form)
        
        # Update lead status if changed
        if form.instance.lead_status_update:
            lead = form.instance.lead
            lead.status = form.instance.lead_status_update
            lead.save()
            
            # Log the change
            LeadHistory.objects.create(
                lead=lead,
                changed_by=self.request.user,
                field_name='status',
                old_value=lead.status,
                new_value=form.instance.lead_status_update,
                notes=f'Status updated via activity {form.instance.activity_id}'
            )
        
        return response
    
    def get_success_url(self):
        # Redirect to lead detail if came from there
        lead_id = self.request.GET.get('lead_id')
        if lead_id:
            return reverse_lazy('newapp:lead_detail', kwargs={'pk': lead_id})
        return reverse_lazy('newapp:activity_list')


class ActivityUpdateView(LoginRequiredMixin, UpdateView):
    model = LeadActivity
    form_class = LeadActivityForm
    template_name = 'newapp/activity_form.html'
    success_url = reverse_lazy('newapp:activity_list')
    login_url = 'newapp:signin'
    
    def get_queryset(self):
        user = self.request.user
        # Admin can edit all activities, sales reps can only edit their leads' activities
        if user.is_staff or user.is_superuser:
            return LeadActivity.objects.all()
        else:
            try:
                sales_employee = user.sales_profile
                return LeadActivity.objects.filter(lead__assigned_to=sales_employee)
            except SalesEmployee.DoesNotExist:
                return LeadActivity.objects.none()
    
    def get_success_url(self):
        return reverse_lazy('newapp:lead_detail', kwargs={'pk': self.object.lead.pk})


class ActivityDetailView(LoginRequiredMixin, DetailView):
    model = LeadActivity
    template_name = 'newapp/activity_detail.html'
    context_object_name = 'activity'
    login_url = 'newapp:signin'


# Activity Dashboard - Follow-up Tracker
class ActivityDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'newapp/activity_dashboard.html'
    login_url = 'newapp:signin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()
        
        # Determine if admin view
        if user.is_staff or user.is_superuser:
            base_queryset = LeadActivity.objects.all()
            context['is_admin'] = True
        else:
            try:
                sales_employee = user.sales_profile
                base_queryset = LeadActivity.objects.filter(lead__assigned_to=sales_employee)
                context['is_admin'] = False
            except SalesEmployee.DoesNotExist:
                base_queryset = LeadActivity.objects.none()
                context['is_admin'] = False
        
        # Overdue follow-ups (scheduled activities in the past)
        context['overdue_followups'] = base_queryset.filter(
            status='SCHEDULED',
            activity_date__lt=today
        ).select_related('lead', 'lead__prospect', 'lead__assigned_to__user').order_by('activity_date')
        
        # Today's follow-ups
        context['todays_followups'] = base_queryset.filter(
            activity_date=today
        ).select_related('lead', 'lead__prospect', 'lead__assigned_to__user').order_by('activity_time')
        
        # Upcoming follow-ups (next 7 days)
        context['upcoming_followups'] = base_queryset.filter(
            activity_date__gt=today,
            activity_date__lte=today + timedelta(days=7)
        ).select_related('lead', 'lead__prospect', 'lead__assigned_to__user').order_by('activity_date', 'activity_time')
        
        # Recent completed activities
        context['recent_activities'] = base_queryset.filter(
            status='COMPLETED'
        ).select_related('lead', 'lead__prospect', 'created_by').order_by('-activity_date', '-activity_time')[:10]
        
        # Statistics
        context['overdue_count'] = context['overdue_followups'].count()
        context['today_count'] = context['todays_followups'].count()
        context['upcoming_count'] = context['upcoming_followups'].count()
        context['total_activities'] = base_queryset.count()
        context['completed_activities'] = base_queryset.filter(status='COMPLETED').count()
        
        # Activity type breakdown
        context['activity_by_type'] = base_queryset.values('activity_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        return context


# ==========================
# QUOTATION MANAGEMENT VIEWS
# ==========================

class QuotationListView(LoginRequiredMixin, ListView):
    model = Quotation
    template_name = 'newapp/quotation_list.html'
    context_object_name = 'quotations'
    paginate_by = 20
    login_url = 'newapp:signin'
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin sees all quotations, sales reps see only their assigned quotations
        if user.is_staff or user.is_superuser:
            queryset = Quotation.objects.all()
        else:
            try:
                sales_employee = user.sales_profile
                queryset = Quotation.objects.filter(assigned_to=sales_employee)
            except SalesEmployee.DoesNotExist:
                queryset = Quotation.objects.none()
        
        queryset = queryset.select_related('prospect', 'assigned_to__user', 'created_by')
        
        # Filter by date range
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(quote_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(quote_date__lte=end_date)
        
        # Filter by salesperson
        salesperson = self.request.GET.get('salesperson')
        if salesperson:
            queryset = queryset.filter(assigned_to__id=salesperson)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by customer
        customer = self.request.GET.get('customer')
        if customer:
            queryset = queryset.filter(prospect__id=customer)
        
        # Filter by amount range
        min_amount = self.request.GET.get('min_amount')
        max_amount = self.request.GET.get('max_amount')
        if min_amount:
            queryset = queryset.filter(net_amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(net_amount__lte=max_amount)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(quote_number__icontains=search) |
                Q(prospect__name__icontains=search) |
                Q(prospect__company_name__icontains=search)
            )
        
        return queryset.order_by('-quote_date', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter options
        context['status_choices'] = Quotation.STATUS_CHOICES
        context['sales_employees'] = SalesEmployee.objects.filter(is_active=True).select_related('user')
        context['prospects'] = ProspectCustomer.objects.all().order_by('name')
        
        # Preserve filter values
        context['current_salesperson'] = self.request.GET.get('salesperson', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_customer'] = self.request.GET.get('customer', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['min_amount'] = self.request.GET.get('min_amount', '')
        context['max_amount'] = self.request.GET.get('max_amount', '')
        context['search'] = self.request.GET.get('search', '')
        
        return context


class QuotationCreateView(LoginRequiredMixin, CreateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'newapp/quotation_form.html'
    login_url = 'newapp:signin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = QuotationItemFormSet(self.request.POST, instance=self.object)
        else:
            context['item_formset'] = QuotationItemFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        
        form.instance.created_by = self.request.user
        form.instance.status = 'DRAFT'
        
        # Set assigned_to to current user's sales profile if not set
        if not form.instance.assigned_to:
            try:
                form.instance.assigned_to = self.request.user.sales_profile
            except SalesEmployee.DoesNotExist:
                pass
        
        if form.is_valid() and item_formset.is_valid():
            self.object = form.save()
            item_formset.instance = self.object
            item_formset.save()
            
            # Update line numbers
            for idx, item in enumerate(self.object.items.all(), start=1):
                item.line_number = idx
                item.save()
            
            # Calculate totals
            self.object.calculate_totals()
            
            # Log activity
            QuotationActivity.objects.create(
                quotation=self.object,
                activity_type='COMMENT',
                description='Quotation created',
                created_by=self.request.user
            )
            
            return redirect('newapp:quotation_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('newapp:quotation_detail', kwargs={'pk': self.object.pk})


class QuotationUpdateView(LoginRequiredMixin, UpdateView):
    model = Quotation
    form_class = QuotationForm
    template_name = 'newapp/quotation_form.html'
    login_url = 'newapp:signin'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Quotation.objects.all()
        else:
            try:
                sales_employee = user.sales_profile
                return Quotation.objects.filter(assigned_to=sales_employee)
            except SalesEmployee.DoesNotExist:
                return Quotation.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = QuotationItemFormSet(self.request.POST, instance=self.object)
        else:
            context['item_formset'] = QuotationItemFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        
        if form.is_valid() and item_formset.is_valid():
            self.object = form.save()
            item_formset.instance = self.object
            item_formset.save()
            
            # Update line numbers
            for idx, item in enumerate(self.object.items.all(), start=1):
                item.line_number = idx
                item.save()
            
            # Calculate totals
            self.object.calculate_totals()
            
            # Log activity
            QuotationActivity.objects.create(
                quotation=self.object,
                activity_type='COMMENT',
                description='Quotation updated',
                created_by=self.request.user
            )
            
            return redirect('newapp:quotation_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('newapp:quotation_detail', kwargs={'pk': self.object.pk})


class QuotationDetailView(LoginRequiredMixin, DetailView):
    model = Quotation
    template_name = 'newapp/quotation_detail.html'
    context_object_name = 'quotation'
    login_url = 'newapp:signin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get items
        context['items'] = self.object.items.all().order_by('line_number')
        
        # Get attachments
        context['attachments'] = self.object.attachments.all().order_by('-uploaded_at')
        
        # Get activities
        context['activities'] = self.object.activities.all().select_related('created_by').order_by('-created_at')
        
        # Add activity form
        context['activity_form'] = QuotationActivityForm()
        
        # Add attachment form
        context['attachment_form'] = QuotationAttachmentForm()
        
        return context


# Additional quotation action views
@login_required(login_url='newapp:signin')
def quotation_send(request, pk):
    """Send quotation to customer"""
    quotation = get_object_or_404(Quotation, pk=pk)
    
    # Check permission
    if not (request.user.is_staff or request.user.sales_profile == quotation.assigned_to):
        return HttpResponse("Unauthorized", status=403)
    
    quotation.status = 'SENT'
    quotation.sent_at = timezone.now()
    quotation.save()
    
    # Log activity
    QuotationActivity.objects.create(
        quotation=quotation,
        activity_type='SENT',
        description=f'Quotation sent to customer by {request.user.get_full_name() or request.user.username}',
        created_by=request.user
    )
    
    return redirect('newapp:quotation_detail', pk=pk)


@login_required(login_url='newapp:signin')
def quotation_approve(request, pk):
    """Approve quotation"""
    quotation = get_object_or_404(Quotation, pk=pk)
    
    # Only staff can approve
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)
    
    quotation.status = 'APPROVED'
    quotation.approved_by = request.user
    quotation.approved_at = timezone.now()
    quotation.save()
    
    # Log activity
    QuotationActivity.objects.create(
        quotation=quotation,
        activity_type='APPROVED',
        description=f'Quotation approved by {request.user.get_full_name() or request.user.username}',
        created_by=request.user
    )
    
    return redirect('newapp:quotation_detail', pk=pk)


@login_required(login_url='newapp:signin')
def quotation_reject(request, pk):
    """Reject quotation"""
    quotation = get_object_or_404(Quotation, pk=pk)
    
    # Only staff can reject
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)
    
    quotation.status = 'REJECTED'
    quotation.save()
    
    # Log activity
    QuotationActivity.objects.create(
        quotation=quotation,
        activity_type='REJECTED',
        description=f'Quotation rejected by {request.user.get_full_name() or request.user.username}',
        created_by=request.user
    )
    
    return redirect('newapp:quotation_detail', pk=pk)


@login_required(login_url='newapp:signin')
def quotation_add_activity(request, pk):
    """Add activity/comment to quotation"""
    quotation = get_object_or_404(Quotation, pk=pk)
    
    if request.method == 'POST':
        form = QuotationActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.quotation = quotation
            activity.created_by = request.user
            activity.save()
    
    return redirect('newapp:quotation_detail', pk=pk)


@login_required(login_url='newapp:signin')
def quotation_add_attachment(request, pk):
    """Add attachment to quotation"""
    quotation = get_object_or_404(Quotation, pk=pk)
    
    if request.method == 'POST':
        form = QuotationAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.quotation = quotation
            attachment.uploaded_by = request.user
            attachment.save()
    
    return redirect('newapp:quotation_detail', pk=pk)


# ==========================
# SALES ORDER MANAGEMENT VIEWS
# ==========================

class SalesOrderListView(LoginRequiredMixin, ListView):
    model = SalesOrder
    template_name = 'newapp/salesorder_list.html'
    context_object_name = 'orders'
    paginate_by = 20
    login_url = 'newapp:signin'
    
    def get_queryset(self):
        user = self.request.user
        
        # Admin sees all orders, sales reps see only their assigned orders
        if user.is_staff or user.is_superuser:
            queryset = SalesOrder.objects.all()
        else:
            try:
                sales_employee = user.sales_profile
                queryset = SalesOrder.objects.filter(assigned_to=sales_employee)
            except SalesEmployee.DoesNotExist:
                queryset = SalesOrder.objects.none()
        
        queryset = queryset.select_related('prospect', 'assigned_to__user', 'created_by')
        
        # Filter by date range
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(order_date__gte=start_date)
        if end_date:
            queryset = queryset.filter(order_date__lte=end_date)
        
        # Filter by salesperson
        salesperson = self.request.GET.get('salesperson')
        if salesperson:
            queryset = queryset.filter(assigned_to__id=salesperson)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by customer
        customer = self.request.GET.get('customer')
        if customer:
            queryset = queryset.filter(prospect__id=customer)
        
        # Filter by amount range
        min_amount = self.request.GET.get('min_amount')
        max_amount = self.request.GET.get('max_amount')
        if min_amount:
            queryset = queryset.filter(net_amount__gte=min_amount)
        if max_amount:
            queryset = queryset.filter(net_amount__lte=max_amount)
        
        # Search
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(order_number__icontains=search) |
                Q(prospect__name__icontains=search) |
                Q(prospect__company_name__icontains=search)
            )
        
        return queryset.order_by('-order_date', '-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add filter options
        context['status_choices'] = SalesOrder.STATUS_CHOICES
        context['sales_employees'] = SalesEmployee.objects.filter(is_active=True).select_related('user')
        context['prospects'] = ProspectCustomer.objects.all().order_by('name')
        
        # Preserve filter values
        context['current_salesperson'] = self.request.GET.get('salesperson', '')
        context['current_status'] = self.request.GET.get('status', '')
        context['current_customer'] = self.request.GET.get('customer', '')
        context['start_date'] = self.request.GET.get('start_date', '')
        context['end_date'] = self.request.GET.get('end_date', '')
        context['min_amount'] = self.request.GET.get('min_amount', '')
        context['max_amount'] = self.request.GET.get('max_amount', '')
        context['search'] = self.request.GET.get('search', '')
        
        return context


class SalesOrderCreateView(LoginRequiredMixin, CreateView):
    model = SalesOrder
    form_class = SalesOrderForm
    template_name = 'newapp/salesorder_form.html'
    login_url = 'newapp:signin'
    
    def get_initial(self):
        """Pre-fill form if creating from quotation"""
        initial = super().get_initial()
        quotation_id = self.request.GET.get('from_quotation')
        
        if quotation_id:
            try:
                quotation = Quotation.objects.get(pk=quotation_id)
                # Copy all fields from quotation to order
                initial.update({
                    'prospect': quotation.prospect,
                    'contact_person': quotation.contact_person,
                    'contact_email': quotation.contact_email,
                    'contact_phone': quotation.contact_phone,
                    'assigned_to': quotation.assigned_to,
                    'currency': quotation.currency,
                    'exchange_rate': quotation.exchange_rate,
                    'payment_terms': quotation.payment_terms,
                    'delivery_terms': quotation.delivery_terms,
                    'reference_lead': quotation.reference_lead,
                    'reference_visit': quotation.reference_visit,
                    'reference_quotation': quotation,
                    'reference_number': quotation.reference_number,
                    'customer_remarks': quotation.customer_remarks,
                    'internal_notes': quotation.internal_notes,
                    'discount_percentage': quotation.discount_percentage,
                    'freight_charges': quotation.freight_charges,
                })
                # Store quotation ID in session for item copying
                self.request.session['source_quotation_id'] = quotation_id
            except Quotation.DoesNotExist:
                pass
        
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quotation_id = self.request.GET.get('from_quotation') or self.request.session.get('source_quotation_id')
        
        if self.request.POST:
            context['item_formset'] = SalesOrderItemFormSet(self.request.POST, instance=self.object)
        else:
            # If creating from quotation, pre-populate items
            if quotation_id and not self.object:
                try:
                    quotation = Quotation.objects.get(pk=quotation_id)
                    context['quotation_items'] = quotation.items.all().order_by('line_number')
                    context['from_quotation'] = True
                except Quotation.DoesNotExist:
                    context['item_formset'] = SalesOrderItemFormSet(instance=self.object)
            else:
                context['item_formset'] = SalesOrderItemFormSet(instance=self.object)
        
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context.get('item_formset')
        
        form.instance.created_by = self.request.user
        form.instance.status = 'DRAFT'
        
        # Set assigned_to to current user's sales profile if not set
        if not form.instance.assigned_to:
            try:
                form.instance.assigned_to = self.request.user.sales_profile
            except SalesEmployee.DoesNotExist:
                pass
        
        # Check if creating from quotation
        quotation_id = self.request.session.get('source_quotation_id')
        from_quotation = context.get('from_quotation', False)
        
        # If item formset exists, validate it
        if item_formset and form.is_valid() and item_formset.is_valid():
            self.object = form.save()
            item_formset.instance = self.object
            item_formset.save()
            
            # Update line numbers
            for idx, item in enumerate(self.object.items.all(), start=1):
                item.line_number = idx
                item.save()
        # If creating from quotation, copy items from quotation
        elif from_quotation and quotation_id and form.is_valid():
            self.object = form.save()
            
            try:
                quotation = Quotation.objects.get(pk=quotation_id)
                # Copy all items from quotation
                for q_item in quotation.items.all().order_by('line_number'):
                    SalesOrderItem.objects.create(
                        order=self.object,
                        item_code=q_item.item_code,
                        description=q_item.description,
                        quantity=q_item.quantity,
                        uom=q_item.uom,
                        unit_price=q_item.unit_price,
                        discount_percentage=q_item.discount_percentage,
                        tax_percentage=q_item.tax_percentage,
                        line_number=q_item.line_number,
                        remarks=q_item.remarks
                    )
                
                # Clear session
                if 'source_quotation_id' in self.request.session:
                    del self.request.session['source_quotation_id']
                    
            except Quotation.DoesNotExist:
                pass
        else:
            return self.render_to_response(self.get_context_data(form=form))
        
        # Calculate totals
        self.object.calculate_totals()
        
        # Log activity
        activity_desc = 'Sales Order created'
        if quotation_id:
            activity_desc = f'Sales Order created from Quotation #{quotation_id}'
        
        SalesOrderActivity.objects.create(
            order=self.object,
            activity_type='COMMENT',
            description=activity_desc,
            created_by=self.request.user
        )
        
        return redirect('newapp:salesorder_detail', pk=self.object.pk)
    
    def get_success_url(self):
        return reverse_lazy('newapp:salesorder_detail', kwargs={'pk': self.object.pk})


class SalesOrderUpdateView(LoginRequiredMixin, UpdateView):
    model = SalesOrder
    form_class = SalesOrderForm
    template_name = 'newapp/salesorder_form.html'
    login_url = 'newapp:signin'
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return SalesOrder.objects.all()
        else:
            try:
                sales_employee = user.sales_profile
                return SalesOrder.objects.filter(assigned_to=sales_employee)
            except SalesEmployee.DoesNotExist:
                return SalesOrder.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['item_formset'] = SalesOrderItemFormSet(self.request.POST, instance=self.object)
        else:
            context['item_formset'] = SalesOrderItemFormSet(instance=self.object)
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        item_formset = context['item_formset']
        
        if form.is_valid() and item_formset.is_valid():
            self.object = form.save()
            item_formset.instance = self.object
            item_formset.save()
            
            # Update line numbers
            for idx, item in enumerate(self.object.items.all(), start=1):
                item.line_number = idx
                item.save()
            
            # Calculate totals
            self.object.calculate_totals()
            
            # Log activity
            SalesOrderActivity.objects.create(
                order=self.object,
                activity_type='COMMENT',
                description='Sales Order updated',
                created_by=self.request.user
            )
            
            return redirect('newapp:salesorder_detail', pk=self.object.pk)
        else:
            return self.render_to_response(self.get_context_data(form=form))
    
    def get_success_url(self):
        return reverse_lazy('newapp:salesorder_detail', kwargs={'pk': self.object.pk})


class SalesOrderDetailView(LoginRequiredMixin, DetailView):
    model = SalesOrder
    template_name = 'newapp/salesorder_detail.html'
    context_object_name = 'order'
    login_url = 'newapp:signin'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get items
        context['items'] = self.object.items.all().order_by('line_number')
        
        # Get attachments
        context['attachments'] = self.object.attachments.all().order_by('-uploaded_at')
        
        # Get activities
        context['activities'] = self.object.activities.all().select_related('created_by').order_by('-created_at')
        
        # Add activity form
        context['activity_form'] = SalesOrderActivityForm()
        
        # Add attachment form
        context['attachment_form'] = SalesOrderAttachmentForm()
        
        return context


# Additional sales order action views
@login_required(login_url='newapp:signin')
def salesorder_confirm(request, pk):
    """Confirm sales order"""
    order = get_object_or_404(SalesOrder, pk=pk)
    
    # Check permission
    if not (request.user.is_staff or request.user.sales_profile == order.assigned_to):
        return HttpResponse("Unauthorized", status=403)
    
    order.status = 'CONFIRMED'
    order.confirmed_at = timezone.now()
    order.save()
    
    # Log activity
    SalesOrderActivity.objects.create(
        order=order,
        activity_type='CONFIRMED',
        description=f'Order confirmed by {request.user.get_full_name() or request.user.username}',
        created_by=request.user
    )
    
    return redirect('newapp:salesorder_detail', pk=pk)


@login_required(login_url='newapp:signin')
def salesorder_approve(request, pk):
    """Approve sales order"""
    order = get_object_or_404(SalesOrder, pk=pk)
    
    # Only staff can approve
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)
    
    order.status = 'APPROVED'
    order.approved_by = request.user
    order.approved_at = timezone.now()
    order.save()
    
    # Log activity
    SalesOrderActivity.objects.create(
        order=order,
        activity_type='APPROVED',
        description=f'Order approved by {request.user.get_full_name() or request.user.username}',
        created_by=request.user
    )
    
    return redirect('newapp:salesorder_detail', pk=pk)


@login_required(login_url='newapp:signin')
def salesorder_reject(request, pk):
    """Reject sales order"""
    order = get_object_or_404(SalesOrder, pk=pk)
    
    # Only staff can reject
    if not request.user.is_staff:
        return HttpResponse("Unauthorized", status=403)
    
    order.status = 'CANCELLED'
    order.save()
    
    # Log activity
    SalesOrderActivity.objects.create(
        order=order,
        activity_type='REJECTED',
        description=f'Order rejected by {request.user.get_full_name() or request.user.username}',
        created_by=request.user
    )
    
    return redirect('newapp:salesorder_detail', pk=pk)


@login_required(login_url='newapp:signin')
def salesorder_add_activity(request, pk):
    """Add activity/comment to sales order"""
    order = get_object_or_404(SalesOrder, pk=pk)
    
    if request.method == 'POST':
        form = SalesOrderActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.order = order
            activity.created_by = request.user
            activity.save()
    
    return redirect('newapp:salesorder_detail', pk=pk)


@login_required(login_url='newapp:signin')
def salesorder_add_attachment(request, pk):
    """Add attachment to sales order"""
    order = get_object_or_404(SalesOrder, pk=pk)
    
    if request.method == 'POST':
        form = SalesOrderAttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.order = order
            attachment.uploaded_by = request.user
            attachment.save()
    
    return redirect('newapp:salesorder_detail', pk=pk)


@login_required(login_url='newapp:signin')
def get_quotation_data(request):
    """API endpoint to fetch quotation data by quote number"""
    from django.http import JsonResponse
    
    quote_number = request.GET.get('quote_number', '').strip()
    
    if not quote_number:
        return JsonResponse({'error': 'Quotation number is required'}, status=400)
    
    try:
        quotation = Quotation.objects.get(quote_number__iexact=quote_number)
        
        # Prepare quotation data
        data = {
            'success': True,
            'quotation': {
                'id': quotation.id,
                'quote_number': quotation.quote_number,
                'prospect_id': quotation.prospect.id,
                'prospect_name': quotation.prospect.name,
                'contact_person': quotation.contact_person,
                'contact_email': quotation.contact_email or '',
                'contact_phone': quotation.contact_phone or '',
                'assigned_to_id': quotation.assigned_to.id if quotation.assigned_to else None,
                'currency': quotation.currency,
                'exchange_rate': str(quotation.exchange_rate),
                'payment_terms': quotation.payment_terms or '',
                'delivery_terms': quotation.delivery_terms or '',
                'reference_lead_id': quotation.reference_lead.id if quotation.reference_lead else None,
                'reference_visit_id': quotation.reference_visit.id if quotation.reference_visit else None,
                'reference_number': quotation.reference_number or '',
                'customer_remarks': quotation.customer_remarks or '',
                'internal_notes': quotation.internal_notes or '',
                'discount_percentage': str(quotation.discount_percentage),
                'freight_charges': str(quotation.freight_charges),
            },
            'items': []
        }
        
        # Add items
        for item in quotation.items.all().order_by('line_number'):
            data['items'].append({
                'line_number': item.line_number,
                'item_code': item.item_code or '',
                'description': item.description,
                'quantity': str(item.quantity),
                'uom': item.uom,
                'unit_price': str(item.unit_price),
                'discount_percentage': str(item.discount_percentage),
                'tax_percentage': str(item.tax_percentage),
                'line_total': str(item.line_total),
                'remarks': item.remarks or '',
            })
        
        return JsonResponse(data)
        
    except Quotation.DoesNotExist:
        return JsonResponse({
            'error': f'Quotation "{quote_number}" not found. Please check the quotation number and try again.'
        }, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='newapp:signin')
def get_item_data(request):
    """API endpoint to fetch item data from Item Master by item code or ID"""
    from django.http import JsonResponse
    from .models import ItemMaster
    
    item_code = request.GET.get('item_code', '').strip()
    item_id = request.GET.get('item_id', '').strip()
    
    if not item_code and not item_id:
        return JsonResponse({'error': 'Item code or ID is required'}, status=400)
    
    try:
        if item_id:
            item = ItemMaster.objects.get(id=item_id, is_active=True)
        else:
            item = ItemMaster.objects.get(item_code__iexact=item_code, is_active=True)
        
        data = {
            'success': True,
            'item': {
                'id': item.id,
                'item_code': item.item_code,
                'description': item.description,
                'short_name': item.short_name or '',
                'item_type': item.item_type,
                'unit_of_measurement': item.unit_of_measurement,
                'standard_price': str(item.standard_price),
                'minimum_price': str(item.minimum_price),
                'purchase_price': str(item.purchase_price) if item.purchase_price else '0.00',
                'hsn_sac_code': item.hsn_sac_code or '',
                'default_tax_percentage': str(item.default_tax_percentage),
                'manufacturer': item.manufacturer or '',
                'brand': item.brand or '',
                'category': item.category or '',
            }
        }
        
        return JsonResponse(data)
        
    except ItemMaster.DoesNotExist:
        return JsonResponse({
            'error': f'Item not found in Item Master or is inactive.'
        }, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required(login_url='newapp:signin')
def search_items(request):
    """API endpoint to search items for autocomplete"""
    from django.http import JsonResponse
    from .models import ItemMaster
    from django.db.models import Q
    
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'items': []})
    
    try:
        items = ItemMaster.objects.filter(
            Q(item_code__icontains=query) | 
            Q(description__icontains=query) |
            Q(short_name__icontains=query),
            is_active=True
        ).order_by('item_code')[:20]  # Limit to 20 results
        
        data = {
            'items': [{
                'id': item.id,
                'item_code': item.item_code,
                'description': item.description[:100],  # Truncate long descriptions
                'unit_price': str(item.standard_price),
                'uom': item.unit_of_measurement,
                'tax_percentage': str(item.default_tax_percentage),
            } for item in items]
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# Additional API endpoints for client-side optimization
@login_required
def search_prospects(request):
    """API endpoint to search prospects for autocomplete"""
    from django.http import JsonResponse
    from .models import ProspectCustomer
    from django.db.models import Q
    
    query = request.GET.get('q', '').strip()
    
    if not query or len(query) < 2:
        return JsonResponse({'items': []})
    
    try:
        prospects = ProspectCustomer.objects.filter(
            Q(name__icontains=query) | 
            Q(company_name__icontains=query) |
            Q(email__icontains=query),
            user=request.user
        ).order_by('name')[:20]  # Limit to 20 results
        
        data = {
            'items': [{
                'id': prospect.id,
                'name': prospect.name,
                'company_name': prospect.company_name or '',
                'email': prospect.email or '',
                'phone': prospect.phone or '',
                'contact_person': prospect.contact_person or '',
                'address': prospect.address or '',
            } for prospect in prospects]
        }
        
        return JsonResponse(data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def get_prospect_data(request):
    """API endpoint to fetch prospect data by name or ID"""
    from django.http import JsonResponse
    from .models import ProspectCustomer
    
    prospect_name = request.GET.get('name', '').strip()
    prospect_id = request.GET.get('id', '').strip()
    
    if not prospect_name and not prospect_id:
        return JsonResponse({'error': 'Prospect name or ID is required'}, status=400)
    
    try:
        if prospect_id:
            prospect = ProspectCustomer.objects.get(id=prospect_id, user=request.user)
        else:
            prospect = ProspectCustomer.objects.get(name__iexact=prospect_name, user=request.user)
        
        data = {
            'success': True,
            'prospect': {
                'id': prospect.id,
                'name': prospect.name,
                'company_name': prospect.company_name or '',
                'email': prospect.email or '',
                'phone': prospect.phone or '',
                'contact_person': prospect.contact_person or '',
                'address': prospect.address or '',
                'status': prospect.status,
            }
        }
        
        return JsonResponse(data)
        
    except ProspectCustomer.DoesNotExist:
        return JsonResponse({'error': 'Prospect not found'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def dashboard_data_api(request):
    """API endpoint for dashboard data with caching headers"""
    from django.http import JsonResponse
    from django.views.decorators.cache import cache_page
    from django.core.cache import cache
    from django.utils import timezone
    from datetime import timedelta
    
    # Check if user has cached data
    cache_key = f"dashboard_data_{request.user.id}"
    cached_data = cache.get(cache_key)
    
    if cached_data:
        return JsonResponse(cached_data)
    
    # Get effective user (admin viewing as another user or current user)
    view_as_user_id = request.GET.get('view_as_user')
    if view_as_user_id and view_as_user_id != 'self' and (request.user.is_staff or request.user.is_superuser):
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(id=view_as_user_id)
        except (ValueError, User.DoesNotExist):
            user = request.user
    else:
        user = request.user
    
    # Date calculations
    today = timezone.now().date()
    month_start = today.replace(day=1)
    week_ago = today - timedelta(days=7)
    
    # Check if admin (and not viewing as specific user)
    is_admin_view = (request.user.is_staff or request.user.is_superuser) and (not view_as_user_id or view_as_user_id == 'self')
    
    if is_admin_view:
        # ADMIN DASHBOARD - Aggregate data across all users
        from .models import VisitLog, ProspectCustomer
        
        # Total Visits (Today / Month)
        visits_today = VisitLog.objects.filter(visit_date=today).count()
        visits_month = VisitLog.objects.filter(visit_date__gte=month_start).count()
        
        # Total Leads (By Stage)
        leads_by_stage = list(ProspectCustomer.objects.values('status').annotate(count=Count('id')).order_by('status'))
        total_leads = ProspectCustomer.objects.count()
        
        # Conversion %
        total_prospects = ProspectCustomer.objects.count()
        converted_prospects = ProspectCustomer.objects.filter(status='WON').count()
        conversion_rate = round((converted_prospects / total_prospects * 100), 1) if total_prospects > 0 else 0
        
        # Upcoming follow-ups
        upcoming_followups = list(VisitLog.objects.filter(
            next_follow_up_date__gte=today,
            next_follow_up_date__lte=today + timedelta(days=7)
        ).select_related('prospect', 'sales_employee__user').values(
            'prospect__name', 'prospect__company_name', 'next_follow_up_date', 
            'visit_date', 'sales_employee__user__first_name', 'sales_employee__user__last_name'
        ))
        
        data = {
            'visits_today': visits_today,
            'visits_month': visits_month,
            'total_leads': total_leads,
            'conversion_rate': conversion_rate,
            'converted_count': converted_prospects,
            'leads_by_stage': leads_by_stage,
            'upcoming_followups': upcoming_followups,
            'timestamp': timezone.now().isoformat()
        }
    else:
        # SALES EXECUTIVE DASHBOARD - User-specific data
        from .models import VisitLog, ProspectCustomer, SalesEmployee
        
        try:
            sales_employee = SalesEmployee.objects.get(user=user)
        except SalesEmployee.DoesNotExist:
            return JsonResponse({'error': 'Sales employee profile not found'}, status=404)
        
        # User's visits
        visits_today = VisitLog.objects.filter(sales_employee=sales_employee, visit_date=today).count()
        visits_month = VisitLog.objects.filter(sales_employee=sales_employee, visit_date__gte=month_start).count()
        
        # User's leads
        leads_by_stage = list(ProspectCustomer.objects.filter(user=user).values('status').annotate(count=Count('id')).order_by('status'))
        total_leads = ProspectCustomer.objects.filter(user=user).count()
        active_leads = ProspectCustomer.objects.filter(user=user, status__in=['NEW', 'CONTACTED', 'QUALIFIED', 'PROPOSAL', 'NEGOTIATION']).count()
        
        # Conversion rate for user
        converted_prospects = ProspectCustomer.objects.filter(user=user, status='WON').count()
        conversion_rate = round((converted_prospects / total_leads * 100), 1) if total_leads > 0 else 0
        
        # User's upcoming follow-ups
        upcoming_followups = list(VisitLog.objects.filter(
            sales_employee=sales_employee,
            next_follow_up_date__gte=today,
            next_follow_up_date__lte=today + timedelta(days=7)
        ).select_related('prospect').values(
            'prospect__name', 'prospect__company_name', 'next_follow_up_date', 'visit_date'
        ))
        
        data = {
            'visits_today': visits_today,
            'visits_month': visits_month,
            'total_leads': total_leads,
            'active_leads': active_leads,
            'conversion_rate': conversion_rate,
            'converted_count': converted_prospects,
            'leads_by_stage': leads_by_stage,
            'upcoming_followups': upcoming_followups,
            'timestamp': timezone.now().isoformat()
        }
    
    # Cache for 5 minutes
    cache.set(cache_key, data, 300)
    
    return JsonResponse(data)


# Service Call Views
class ServiceCallListView(LoginRequiredMixin, ListView):
    """List view for service calls with filtering and search"""
    model = ServiceCall
    template_name = 'newapp/servicecall_list.html'
    context_object_name = 'service_calls'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = ServiceCall.objects.select_related(
            'customer', 'assigned_technician', 'created_by'
        ).order_by('-created_at')
        
        # Filter by user if not admin
        if not self.request.user.is_staff:
            try:
                sales_employee = SalesEmployee.objects.get(user=self.request.user)
                queryset = queryset.filter(assigned_technician=sales_employee)
            except SalesEmployee.DoesNotExist:
                queryset = queryset.none()
        
        # Search functionality
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(customer__name__icontains=search_query) |
                Q(contact_person__icontains=search_query) |
                Q(service_type__icontains=search_query) |
                Q(problem_description__icontains=search_query)
            )
        
        # Filter by status
        status_filter = self.request.GET.get('status', '')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by priority
        priority_filter = self.request.GET.get('priority', '')
        if priority_filter:
            queryset = queryset.filter(priority=priority_filter)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['status_filter'] = self.request.GET.get('status', '')
        context['priority_filter'] = self.request.GET.get('priority', '')
        context['status_choices'] = ServiceCall.STATUS_CHOICES
        context['priority_choices'] = ServiceCall.PRIORITY_CHOICES
        return context
    
    def servicecall_create(request):
        if request.method == 'POST':
            form = ServiceCallForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.created_by = request.user
            obj.save()
            return redirect('newapp:servicecall_list')
        else:
            form = ServiceCallForm()

        return render(request, 'newapp/servicecall_form.html', {'form': form})



class ServiceCallCreateView(LoginRequiredMixin, CreateView):
    """Create view for service calls"""
    model = ServiceCall
    form_class = ServiceCallForm
    template_name = 'newapp/servicecall_form.html'
    success_url = reverse_lazy('newapp:servicecall_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items_formset'] = ServiceCallItemFormSet(self.request.POST)
        else:
            # For new service calls, show one empty form
            context['items_formset'] = ServiceCallItemFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        
        if items_formset.is_valid():
            self.object = form.save()
            items_formset.instance = self.object
            items_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)


class ServiceCallDetailView(LoginRequiredMixin, DetailView):
    """Detail view for service calls"""
    model = ServiceCall
    template_name = 'newapp/servicecall_detail.html'
    context_object_name = 'service_call'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['items'] = self.object.items.select_related('item_master')
        context['attachments'] = self.object.attachments.order_by('-uploaded_at')
        context['activities'] = self.object.activities.order_by('-activity_date', '-start_time')
        return context


class ServiceCallUpdateView(LoginRequiredMixin, UpdateView):
    """Update view for service calls"""
    model = ServiceCall
    form_class = ServiceCallForm
    template_name = 'newapp/servicecall_form.html'
    success_url = reverse_lazy('newapp:servicecall_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['items_formset'] = ServiceCallItemFormSet(
                self.request.POST, instance=self.object
            )
        else:
            # Ensure only one form is shown (existing item if any, otherwise empty form)
            formset = ServiceCallItemFormSet(instance=self.object)
            # If editing and item exists, limit to existing item only
            if self.object and self.object.items.exists():
                # Only show the first existing item
                context['items_formset'] = formset
            else:
                # For new or empty, show one empty form
                context['items_formset'] = formset
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        items_formset = context['items_formset']
        
        if items_formset.is_valid():
            self.object = form.save()
            items_formset.instance = self.object
            items_formset.save()
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
