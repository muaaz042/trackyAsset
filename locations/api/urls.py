from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BuildingViewSet, FloorViewSet, DepartmentViewSet, 
    RoomCategoryViewSet, RoomViewSet
)

router = DefaultRouter()
router.register('buildings', BuildingViewSet, basename='buildings')
router.register('floors', FloorViewSet, basename='floors')
router.register('departments', DepartmentViewSet, basename='departments')
router.register('room-categories', RoomCategoryViewSet, basename='room-categories')
router.register('rooms', RoomViewSet, basename='rooms')

urlpatterns = [
    path('', include(router.urls)),
]