from django.urls import path
from users.api.views import LoginView, MeView, ChangePasswordView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='users-me'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
]