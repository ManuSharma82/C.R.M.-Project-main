from django.urls import path
from . import views

app_name = 'newapp'

urlpatterns = [
    # Authentication
    path('', views.IndexView.as_view(), name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    
    # Prospect Management
    path('prospects/', views.ProspectListView.as_view(), name='prospect_list'),
    path('prospects/create/', views.ProspectCreateView.as_view(), name='prospect_create'),
    path('prospects/<int:pk>/', views.ProspectDetailView.as_view(), name='prospect_detail'),
    path('prospects/<int:pk>/edit/', views.ProspectUpdateView.as_view(), name='prospect_edit'),
    
    # Visit Management
    path('visits/', views.VisitManagementView.as_view(), name='visit_management'),
    path('visits/old/', views.VisitListView.as_view(), name='visit_list'),
    path('visits/create/', views.VisitCreateView.as_view(), name='visit_create'),
    path('visits/<int:pk>/', views.VisitDetailView.as_view(), name='visit_detail'),
    path('visits/<int:pk>/edit/', views.VisitUpdateView.as_view(), name='visit_edit'),
    path('visits/<int:pk>/approve/', views.approve_visit, name='visit_approve') ,
    
    # Reports
    path('reports/visits/', views.VisitReportView.as_view(), name='visit_report'),
    
    # Lead Management
    path('leads/', views.LeadListView.as_view(), name='lead_list'),
    path('leads/create/', views.LeadCreateView.as_view(), name='lead_create'),
    path('leads/<int:pk>/', views.LeadDetailView.as_view(), name='lead_detail'),
    path('leads/<int:pk>/edit/', views.LeadUpdateView.as_view(), name='lead_edit'),
    
    # Activity Tracker / Follow-up Management
    path('activities/', views.ActivityListView.as_view(), name='activity_list'),
    path('activities/dashboard/', views.ActivityDashboardView.as_view(), name='activity_dashboard'),
    path('activities/create/', views.ActivityCreateView.as_view(), name='activity_create'),
    path('activities/<int:pk>/', views.ActivityDetailView.as_view(), name='activity_detail'),
    path('activities/<int:pk>/edit/', views.ActivityUpdateView.as_view(), name='activity_edit'),
    
    # Quotation Management
    path('quotations/', views.QuotationListView.as_view(), name='quotation_list'),
    path('quotations/create/', views.QuotationCreateView.as_view(), name='quotation_create'),
    path('quotations/<int:pk>/', views.QuotationDetailView.as_view(), name='quotation_detail'),
    path('quotations/<int:pk>/edit/', views.QuotationUpdateView.as_view(), name='quotation_edit'),
    path('quotations/<int:pk>/send/', views.quotation_send, name='quotation_send'),
    path('quotations/<int:pk>/approve/', views.quotation_approve, name='quotation_approve'),
    path('quotations/<int:pk>/reject/', views.quotation_reject, name='quotation_reject'),
    path('quotations/<int:pk>/add-activity/', views.quotation_add_activity, name='quotation_add_activity'),
    path('quotations/<int:pk>/add-attachment/', views.quotation_add_attachment, name='quotation_add_attachment'),
    
    # Sales Order Management
    path('orders/', views.SalesOrderListView.as_view(), name='salesorder_list'),
    path('orders/create/', views.SalesOrderCreateView.as_view(), name='salesorder_create'),
    path('orders/<int:pk>/', views.SalesOrderDetailView.as_view(), name='salesorder_detail'),
    path('orders/<int:pk>/edit/', views.SalesOrderUpdateView.as_view(), name='salesorder_edit'),
    path('orders/<int:pk>/confirm/', views.salesorder_confirm, name='salesorder_confirm'),
    path('orders/<int:pk>/approve/', views.salesorder_approve, name='salesorder_approve'),
    path('orders/<int:pk>/reject/', views.salesorder_reject, name='salesorder_reject'),
    path('orders/<int:pk>/add-activity/', views.salesorder_add_activity, name='salesorder_add_activity'),
    path('orders/<int:pk>/add-attachment/', views.salesorder_add_attachment, name='salesorder_add_attachment'),
    
    # Service Call Management
    path('service-calls/', views.ServiceCallListView.as_view(), name='servicecall_list'),
    path('service-calls/create/', views.ServiceCallCreateView.as_view(), name='servicecall_create'),
    path('service-calls/<int:pk>/', views.ServiceCallDetailView.as_view(), name='servicecall_detail'),
    path('service-calls/<int:pk>/edit/', views.ServiceCallUpdateView.as_view(), name='servicecall_edit'),
    
    # API Endpoints
    path('api/get-quotation/', views.get_quotation_data, name='get_quotation_data'),
    path('api/get-item/', views.get_item_data, name='get_item_data'),
    path('api/search-items/', views.search_items, name='search_items'),
    path('api/search-prospects/', views.search_prospects, name='search_prospects'),
    path('api/get-prospect/', views.get_prospect_data, name='get_prospect_data'),
    path('api/dashboard-data/', views.dashboard_data_api, name='dashboard_data_api'),
    path('api/dashboard-updates/', views.dashboard_data_api, name='dashboard_updates_legacy'),
]
