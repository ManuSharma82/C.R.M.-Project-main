"""
Context processors for making data available to all templates
"""
from .models import SalesEmployee


def admin_context(request):
    """
    Add admin-related context to all templates
    """
    context = {}
    
    # Only for staff/admin users
    if request.user.is_authenticated and (request.user.is_staff or request.user.is_superuser):
        # Get all employees for the dropdown
        context['all_employees'] = SalesEmployee.objects.select_related('user').order_by('user__first_name', 'user__last_name')
        
        # Check if admin is viewing as another user
        view_as_user_id = request.GET.get('view_as_user')
        if view_as_user_id and view_as_user_id != 'self':
            try:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                viewed_user = User.objects.get(id=view_as_user_id)
                context['viewing_as_user'] = viewed_user
                context['is_admin_view'] = True
                
                # Try to get sales employee profile
                try:
                    context['viewed_employee'] = viewed_user.sales_profile
                except SalesEmployee.DoesNotExist:
                    context['viewed_employee'] = None
            except (ValueError, User.DoesNotExist):
                pass
    
    return context
