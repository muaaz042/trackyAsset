from users.models import User

def get_user_by_email(email: str) -> User | None:
    return User.objects.filter(email=email).first()

def get_user_me(user: User) -> User:
    """
    Returns the fresh instance of the currently logged-in user 
    with related tenant/building info loaded.
    """
    return User.objects.select_related('tenant', 'assigned_building').get(id=user.id)