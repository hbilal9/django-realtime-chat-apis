from rest_framework import serializers
from api.models import User

class LoginSerializer(serializers.Serializer):
    # username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

class UserSerializer(serializers.ModelSerializer):
    account_type = serializers.CharField(read_only=True)
    role = serializers.CharField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)
    # user_permissions = serializers.ListField(read_only=True)
    is_email_verified = serializers.BooleanField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 'role',
            'account_type', 'is_active', 'date_joined', 'gender', 'phone', 'is_email_verified',
            'user_permissions', 'last_login', 'avatar', 'cover', 'remarks',
        ]

    def validate_email(self, value):
        user = self.context['request'].user
        if value and value != user.email:
            try:
                User.objects.get(email=value)
                raise serializers.ValidationError("Email is already taken.")
            except User.DoesNotExist:
                pass
        return value