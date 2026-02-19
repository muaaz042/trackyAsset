from django.core.exceptions import ValidationError
from locations.models import Building, Floor, Department, RoomCategory, Room

def create_building(user, data):
    # Automatically attach tenant from the creator
    data['tenant'] = user.tenant
    building = Building(**data)
    building.full_clean()
    building.save()
    return building

def create_floor(user, data):
    # Validate building belongs to user's tenant
    if data['building'].tenant != user.tenant:
        raise ValidationError("Cannot create floor in another tenant's building.")
    
    floor = Floor(**data)
    floor.save()
    return floor

def create_room(user, data):
    # Room specific validation is in Model.clean(), but we call it here
    room = Room(**data)
    room.full_clean() # Triggers the logic for checking dept vs category
    room.save()
    return room