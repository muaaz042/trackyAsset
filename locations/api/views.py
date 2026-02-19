from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from locations.models import Building, Floor, Department, RoomCategory, Room
from locations.api import serializers
from locations.api.permissions import LocationAccessPolicy
from locations.api.pagination import StandardResultsSetPagination
from locations.api import filters
from locations.selectors import queries
from locations.services import business_logic

class BuildingViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BuildingSerializer
    permission_classes = [LocationAccessPolicy]
    pagination_class = StandardResultsSetPagination
    filter_backends = [SearchFilter]
    search_fields = ['name', 'address']

    def get_queryset(self):
        return queries.get_buildings(self.request.user)

    def perform_create(self, serializer):
        business_logic.create_building(self.request.user, serializer.validated_data)



class FloorViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.FloorSerializer
    permission_classes = [LocationAccessPolicy]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = filters.FloorFilter
    search_fields = ['name']

    def get_queryset(self):
        return queries.get_floors(self.request.user)

    def perform_create(self, serializer):
        business_logic.create_floor(self.request.user, serializer.validated_data)


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DepartmentSerializer
    permission_classes = [LocationAccessPolicy]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = filters.DepartmentFilter
    search_fields = ['name']

    def get_queryset(self):
        return queries.get_departments(self.request.user)


class RoomCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RoomCategorySerializer
    permission_classes = [LocationAccessPolicy]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['floor']

    def get_queryset(self):
        return queries.get_room_categories(self.request.user)


class RoomViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RoomSerializer
    permission_classes = [LocationAccessPolicy]
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = filters.RoomFilter
    search_fields = ['name']

    def get_queryset(self):
        return queries.get_rooms(self.request.user)

    def perform_create(self, serializer):
        business_logic.create_room(self.request.user, serializer.validated_data)