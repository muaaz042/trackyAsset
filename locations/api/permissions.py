from rest_framework import permissions

class LocationAccessPolicy(permissions.BasePermission):
    """
    Super Admin: Full Access.
    Tenant Admin: Access to all buildings in their tenant.
    Tenant Manager: Read-only access to their ASSIGNED building only.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # 1. Super Admin
        if request.user.is_superuser:
            return True

        # 2. Check User's Tenant vs Object's Tenant
        # We need to traverse up the hierarchy to find the Tenant for the object
        obj_tenant = self._get_tenant_from_object(obj)
        user_tenant = getattr(request.user, 'tenant', None)

        if obj_tenant != user_tenant:
            return False

        # 3. Check Role
        role = getattr(request.user, 'role', '')
        
        if role == 'admin':
            return True # Tenant Admin has full access to their tenant's locations
        
        if role == 'manager':
            # Managers usually only View (GET), unless you want them to edit rooms.
            # Assuming Managers are Read-Only for structural changes:
            if request.method not in permissions.SAFE_METHODS:
                return False

            # Check if this object belongs to the manager's assigned building
            # Assuming User model has `assigned_building` FK
            assigned_building = getattr(request.user, 'assigned_building', None)
            if not assigned_building:
                return False
            
            obj_building = self._get_building_from_object(obj)
            return obj_building == assigned_building

        return False

    def _get_tenant_from_object(self, obj):
        """Helper to find tenant from any location model"""
        if hasattr(obj, 'tenant'): return obj.tenant                   # Building
        if hasattr(obj, 'building'): return obj.building.tenant        # Floor
        if hasattr(obj, 'floor'): return obj.floor.building.tenant     # Dept/Category
        # Room
        if hasattr(obj, 'department') and obj.department: 
            return obj.department.floor.building.tenant
        if hasattr(obj, 'room_category') and obj.room_category: 
            return obj.room_category.floor.building.tenant
        return None

    def _get_building_from_object(self, obj):
        """Helper to find building from any location model"""
        if hasattr(obj, 'tenant'): return obj # It is a building
        if hasattr(obj, 'building'): return obj.building
        if hasattr(obj, 'floor'): return obj.floor.building
        if hasattr(obj, 'department') and obj.department: 
            return obj.department.floor.building
        if hasattr(obj, 'room_category') and obj.room_category: 
            return obj.room_category.floor.building
        return None