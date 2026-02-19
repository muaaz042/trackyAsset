from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User
from .forms import CustomUserCreationForm, CustomUserChangeForm

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    
    ordering = ['email']
    list_display = ('email', 'first_name', 'last_name', 'role', 'tenant', 'assigned_building', 'is_active')
    search_fields = ('email', 'first_name', 'last_name', 'tenant__company_name')
    list_filter = ('role', 'is_active', 'tenant')

    # Fieldsets for editing an existing user
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser')}),
        ('Assignment', {'fields': ('tenant', 'assigned_building')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fieldsets for adding a NEW user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 
                'first_name', 'last_name', 
                'role', 
                'tenant', 'assigned_building',
                'password', 'confirm_password'  # <--- MATCHES NEW FORM NAMES
            ),
        }),
    )