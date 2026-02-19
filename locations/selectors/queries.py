from django.db.models import Q
from locations.models import Building, Floor, Department, RoomCategory, Room

def get_buildings(user):
    if user.is_superuser:
        return Building.objects.all()
    
    # Base filter: User's Tenant
    qs = Building.objects.filter(tenant=user.tenant)
    
    # Manager filter: Assigned Building only
    if getattr(user, 'role', '') == 'manager':
        assigned_building = getattr(user, 'assigned_building', None)
        if assigned_building:
            qs = qs.filter(id=assigned_building.id)
        else:
            return Building.objects.none() # Manager with no building assigned
            
    return qs

def get_floors(user):
    # Get available buildings first to ensure security cascade
    allowed_buildings = get_buildings(user)
    return Floor.objects.filter(building__in=allowed_buildings)

def get_departments(user):
    allowed_floors = get_floors(user)
    return Department.objects.filter(floor__in=allowed_floors)

def get_room_categories(user):
    allowed_floors = get_floors(user)
    return RoomCategory.objects.filter(floor__in=allowed_floors)

def get_rooms(user):
    allowed_floors = get_floors(user)
    # Rooms belong to dept OR category, both connect to floor
    return Room.objects.filter(
        Q(department__floor__in=allowed_floors) | 
        Q(room_category__floor__in=allowed_floors)
    )