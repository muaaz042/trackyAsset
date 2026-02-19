import django_filters
from django.db.models import Q
from locations.models import Building, Floor, Department, RoomCategory, Room

class FloorFilter(django_filters.FilterSet):
    building = django_filters.NumberFilter(field_name='building__id')
    class Meta:
        model = Floor
        fields = ['building', 'name']

class DepartmentFilter(django_filters.FilterSet):
    building = django_filters.NumberFilter(field_name='floor__building__id')
    floor = django_filters.NumberFilter(field_name='floor__id')
    class Meta:
        model = Department
        fields = ['floor', 'building', 'name']

class RoomFilter(django_filters.FilterSet):
    department = django_filters.NumberFilter(field_name='department__id')
    room_category = django_filters.NumberFilter(field_name='room_category__id')
    floor = django_filters.NumberFilter(method='filter_by_floor')
    
    class Meta:
        model = Room
        fields = ['name']

    def filter_by_floor(self, queryset, name, value):
        return queryset.filter(
            Q(department__floor__id=value) | 
            Q(room_category__floor__id=value)
        )