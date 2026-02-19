from rest_framework import serializers
from django.contrib.auth import authenticate
from users.models import User
from tenants.api.serializers import TenantSerializer
from locations.api.serializers import BuildingSerializer

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for listing/viewing users.
    """
    tenant_detail = TenantSerializer(source='tenant', read_only=True)
    building_detail = BuildingSerializer(source='assigned_building', read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 
            'role', 'tenant', 'tenant_detail',
            'assigned_building', 'building_detail', 'is_active'
        ]

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if not user:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'email' and 'password'.")

        data['user'] = user
        return data

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)