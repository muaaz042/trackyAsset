import django_filters
from tenants.models import Tenant

class TenantFilter(django_filters.FilterSet):
    company_name = django_filters.CharFilter(lookup_expr='icontains')
    ntn_number = django_filters.CharFilter(lookup_expr='exact')

    class Meta:
        model = Tenant
        fields = ['company_name', 'ntn_number', 'tenant_prefix']