from rest_framework import serializers
from api.models import User
import re

class LoginSerializer(serializers.Serializer):
    # username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    def validate_username(self, value):
        pattern = r"^[a-zA-Z][a-zA-Z0-9_.]*$"
        if not re.match(pattern, value):
            raise serializers.ValidationError(
                'Invalid username. It should start with a letter and can contain letters, numbers, underscores, and dots.'
            )
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists.")
        if value.len() < 5:
            raise serializers.ValidationError("Username must be at least 5 characters long.")
        return value

    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.pop('confirm_password')
    
    def validate_username(self, username):
        try:
            User.objects.get(username=username)
            raise serializers.ValidationError("This username already exists.")
        except User.DoesNotExist:
            pass
        pattern = r"^[a-zA-Z][a-zA-Z0-9_.]*$"
        if not re.match(pattern, username):
            raise serializers.ValidationError(
                'Invalid username. It should start with a letter and can contain letters, numbers, underscores, and dots.'
            )
        return username
    def validate_email(self, value):
        try:
            User.objects.get(email=value)
            raise serializers.ValidationError("This email already exists.")
        except User.DoesNotExist:
            pass
        return value
    
    def validate_password(self, password):
        if len(password) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if password != self.initial_data['confirm_password']:
            raise serializers.ValidationError("Confirm password must match.")
        return password

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