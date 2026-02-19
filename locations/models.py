from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from tenants.models import Tenant

class Building(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, related_name='buildings')
    name = models.CharField(max_length=255)
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.tenant.company_name})"

class Floor(models.Model):
    building = models.ForeignKey(Building, on_delete=models.CASCADE, related_name='floors')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} - {self.building.name}"

class Department(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.floor.name})"

class RoomCategory(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, related_name='room_categories')
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.floor.name})"

class Room(models.Model):
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, 
        null=True, blank=True, related_name='rooms'
    )
    room_category = models.ForeignKey(
        RoomCategory, on_delete=models.CASCADE, 
        null=True, blank=True, related_name='rooms'
    )
    name = models.CharField(max_length=255)

    def clean(self):
        if not self.department and not self.room_category:
            raise ValidationError(_("A Room must belong to either a Department or a Room Category."))
        if self.department and self.room_category:
            raise ValidationError(_("A Room cannot belong to both a Department and a Room Category simultaneously."))

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name