from rest_framework import serializers
from .models import Login, ErrorMessage

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['email', 'password']

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['name', 'email', 'role' , 'image', 'password']

class ErrorMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ErrorMessage
        fields = ['code', 'message']