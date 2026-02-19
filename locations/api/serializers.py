from rest_framework import serializers
from locations.models import Building, Floor, Department, RoomCategory, Room

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = ['id', 'name', 'address', 'tenant']
        read_only_fields = ['tenant'] # Tenant is set automatically

class FloorSerializer(serializers.ModelSerializer):
    building_name = serializers.CharField(source='building.name', read_only=True)
    class Meta:
        model = Floor
        fields = ['id', 'name', 'building', 'building_name']

class DepartmentSerializer(serializers.ModelSerializer):
    floor_name = serializers.CharField(source='floor.name', read_only=True)
    class Meta:
        model = Department
        fields = ['id', 'name', 'floor', 'floor_name']

class RoomCategorySerializer(serializers.ModelSerializer):
    floor_name = serializers.CharField(source='floor.name', read_only=True)
    class Meta:
        model = RoomCategory
        fields = ['id', 'name', 'floor', 'floor_name']

class RoomSerializer(serializers.ModelSerializer):
    location_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Room
        fields = ['id', 'name', 'department', 'room_category', 'location_name']

    def get_location_name(self, obj):
        if obj.department:
            return f"{obj.department.name} (Dept)"
        return f"{obj.room_category.name} (Cat)" if obj.room_category else "Unknown"

    def validate(self, data):
        """
        DRF level validation for the XOR logic
        """
        department = data.get('department')
        category = data.get('room_category')

        if not department and not category:
            raise serializers.ValidationError("A Room must belong to either a Department or a Room Category.")
        if department and category:
            raise serializers.ValidationError("Select either a Department OR a Category, not both.")
        return data