from rest_framework import serializers
from tenants.models import Tenant

class TenantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tenant
        fields = [
            'id',
            'company_name',
            'business_name',
            'address',
            'ntn_number',
            'ntn_expiry_date',
            'subscription_expiry_date',
            'tenant_prefix',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']