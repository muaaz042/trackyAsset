from django.contrib import admin
from .models import Tenant

@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'tenant_prefix', 'ntn_number', 'subscription_expiry_date')
    search_fields = ('company_name', 'business_name', 'ntn_number')
    list_filter = ('subscription_expiry_date',)

    @admin.display(boolean=True, description='Subscription Active')
    def is_active_subscription(self, obj):
        from django.utils import timezone
        return obj.subscription_expiry_date >= timezone.now().date()