from rest_framework import serializers
from .models import User, Company


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    company = serializers.PrimaryKeyRelatedField(
        queryset=Company.objects.all(),
        required=False
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'role', 'company']

    def validate_role(self, value):
        if value == User.Role.ADMIN:
            raise serializers.ValidationError(
                'Admin accounts cannot be created by registration.'
            )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)