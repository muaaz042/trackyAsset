from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from tenants.api.serializers import TenantSerializer
from tenants.api.permissions import TenantAccessPolicy
from tenants.api.filters import TenantFilter
from tenants.selectors import queries
from tenants.services import business_logic

class TenantViewSet(viewsets.ModelViewSet):
    serializer_class = TenantSerializer
    permission_classes = [TenantAccessPolicy]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = TenantFilter
    ordering_fields = ['created_at', 'subscription_expiry_date']
    ordering = ['-created_at']

    def get_queryset(self):
        """
        Delegates to selectors to filter based on who is logged in.
        Super Admin sees all; Tenant Admin sees only their own.
        """
        return queries.get_tenants(user=self.request.user)

    def perform_create(self, serializer):
        business_logic.create_tenant(data=serializer.validated_data)

    def perform_update(self, serializer):
        business_logic.update_tenant(
            tenant=serializer.instance, 
            data=serializer.validated_data
        )