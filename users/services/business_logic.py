from django.core.exceptions import ValidationError
from django.contrib.auth import authenticate
from users.models import User

def change_password(user: User, old_password: str, new_password: str):
    """
    Validates old password and sets the new one.
    """
    if not user.check_password(old_password):
        raise ValidationError({"old_password": "Wrong old password."})

    user.set_password(new_password)
    user.save()
    return user

def validate_user_assignment(user: User):
    """
    Business logic to ensure roles match assignments.
    Usually called before saving or in serializer validation.
    """
    if user.role == 'admin' and not user.tenant:
        raise ValidationError("Admins must be assigned to a Tenant.")
    
    if user.role == 'manager':
        if not user.tenant:
            raise ValidationError("Managers must be assigned to a Tenant.")
        if not user.assigned_building:
            raise ValidationError("Managers must be assigned to a Building.")
        if user.assigned_building.tenant != user.tenant:
            raise ValidationError("Assigned building does not belong to the assigned tenant.")