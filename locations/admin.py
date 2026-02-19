from django.contrib import admin
from .models import Building, Floor, Department, RoomCategory, Room

class FloorInline(admin.TabularInline):
    model = Floor
    extra = 1

@admin.register(Building)
class BuildingAdmin(admin.ModelAdmin):
    list_display = ('name', 'tenant', 'address')
    list_filter = ('tenant',)
    inlines = [FloorInline]

@admin.register(Floor)
class FloorAdmin(admin.ModelAdmin):
    list_display = ('name', 'building')
    list_filter = ('building__tenant', 'building')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'floor')

@admin.register(RoomCategory)
class RoomCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'floor')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_parent_location')

    @admin.display(description='Location')
    def get_parent_location(self, obj):
        return obj.department if obj.department else obj.room_category