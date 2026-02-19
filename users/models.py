from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

from tenants.models import Tenant
from locations.models import Building

# REMOVED: from users.services import business_logic  <-- Caused the error

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'super_admin')
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    ROLE_CHOICES = (
        ('super_admin', 'Super Admin'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
    )

    username = None
    email = models.EmailField(_('email address'), unique=True)
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='manager')
    
    tenant = models.ForeignKey(
        Tenant, on_delete=models.SET_NULL, null=True, blank=True, related_name='users'
    )
    assigned_building = models.ForeignKey(
        Building, on_delete=models.SET_NULL, null=True, blank=True, related_name='managers'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    @property
    def is_manager(self):
        return self.role == 'manager'

    @property
    def is_tenant_admin(self):
        return self.role == 'admin'

    def clean(self):
        super().clean()
        # FIX: Import here to avoid circular dependency
        from users.services import business_logic 
        business_logic.validate_user_assignment(self)

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)