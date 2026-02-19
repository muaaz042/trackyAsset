from typing import Optional
from django.db.models import QuerySet
from tenants.models import Tenant

def get_tenants(user) -> QuerySet[Tenant]:
    """
    Returns tenants based on user role.
    Super Admin -> All Tenants
    Tenant Admin/User -> Only their own Tenant
    """
    if user.is_superuser:
        return Tenant.objects.all()
    
    # Assuming the User model (to be built) has a 'tenant' field
    if hasattr(user, 'tenant') and user.tenant:
        return Tenant.objects.filter(id=user.tenant.id)
    
    return Tenant.objects.none()

def get_tenant_by_id(*, tenant_id: int) -> Optional[Tenant]:
    try:
        return Tenant.objects.get(id=tenant_id)
    except Tenant.DoesNotExist:
        return None