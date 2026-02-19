from tenants.models import Tenant
from typing import Any, Dict

def create_tenant(*, data: Dict[str, Any]) -> Tenant:
    if 'tenant_prefix' in data:
        data['tenant_prefix'] = data['tenant_prefix'].upper()

    tenant = Tenant(**data)
    tenant.full_clean()
    tenant.save()
    return tenant

def update_tenant(*, tenant: Tenant, data: Dict[str, Any]) -> Tenant:
    for field, value in data.items():
        if field == 'tenant_prefix':
            value = value.upper()
        setattr(tenant, field, value)

    tenant.full_clean()
    tenant.save()
    return tenant