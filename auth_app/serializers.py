from rest_framework import serializers
from .models import Login, ErrorMessage, LoginPayload, LoginResponse

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)
    def create(self, validated_data):
        return LoginPayload(**validated_data)

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['name', 'email', 'role' , 'image', 'password']
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Profile
        fields = ['email', 'role']
        
class ErrorMessageSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=80)
    message =  serializers.CharField(max_length=80)
    def create(self, validated_data):
        return ErrorMessage(**validated_data)
    

class LoginResponseSerializer(serializers.Serializer):
    accessToken  = serializers.CharField(max_length=1000)
    refreshToken = serializers.CharField(max_length=1000)
    
    def create(self, validated_data):
        return LoginResponse(**validated_data)
    