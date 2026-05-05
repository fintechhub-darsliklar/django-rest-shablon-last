from rest_framework import serializers
from apps.users.models import User
from rest_framework.exceptions import ValidationError


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password']

    def validate_first_name(self, obj):
        if len(obj) < 2:
            raise ValidationError("First name must be length more 5")
        return obj
    
