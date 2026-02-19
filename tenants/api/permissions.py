from rest_framework import permissions

class TenantAccessPolicy(permissions.BasePermission):
    """
    Super Admin: Can Create, Read, Update, Delete.
    Tenant Admin: Can Read and Update (Own Tenant only). NO Delete, NO Create.
    """

    def has_permission(self, request, view):
        # 1. Allow strictly authenticated users
        if not request.user.is_authenticated:
            return False

        # 2. CREATE: Only Super Admin can create new tenants
        if view.action == 'create':
            return request.user.is_superuser

        # 3. LIST/RETRIEVE/UPDATE/DELETE: Check logic below or in has_object_permission
        return True

    def has_object_permission(self, request, view, obj):
        # 1. Super Admin has full access
        if request.user.is_superuser:
            return True

        # 2. DELETE: Strictly Super Admin only
        if view.action == 'destroy':
            return False

        # 3. Tenant Admin Access (Read/Update)
        # We assume the upcoming User model has a 'tenant' relation and a role check.
        # Logic: User must belong to this tenant AND be an 'admin' or 'manager' (if managers can view).
        
        user_tenant = getattr(request.user, 'tenant', None)
        
        # Check if user belongs to this tenant
        if user_tenant == obj:
            # If action is update/partial_update, ensure user is a Tenant Admin (not just a manager)
            if view.action in ['update', 'partial_update']:
                # Placeholder: Adjust 'is_tenant_admin' based on your future User model logic
                # e.g., return request.user.role == 'admin'
                return getattr(request.user, 'role', '') == 'admin' or request.user.is_staff
            
            # Read access (GET) allowed for all tenant members
            return True

        return False