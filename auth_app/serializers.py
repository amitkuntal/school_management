from rest_framework import serializers
from .models import *

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['userid', 'schoolname', 'address1', 'address2' , 'address3', 'city', 'state', 'zip']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['userid', 'mobile']

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['userid', 'schoolid', 'classid', 'dob', 'fathername', 'mothername', 'address1', 'address2' , 'address3', 'city', 'state', 'zip', 'admissiondate', 'srno', 'promotedclassid']

class FeeStructureSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeStructure
        fields = ['classid', 'feename', 'cycle' , 'amount'] 

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['userid', 'classid', 'attendancedate' , 'status']

class ClassSerializer(serializers.ModelSerializer):
    class Meta:
        model = Class
        fields = ['schoolid', 'classname', 'classsection']

class FeeDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeDeposit
        fields = ['userid', 'feestructureid', 'depositdate' , 'depositamount']

class HomeworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Homework
        fields = ['userid', 'homework', 'homeworkdate']        

class TranferCertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferCertificate
        fields = ['userid', 'requestedby', 'approveby' , 'requesteddate', 'approvedate', 'status']        

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=100, required=True)
    def create(self, validated_data):
        return LoginPayload(**validated_data)

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = ['name', 'email', 'role' , 'image', 'password']
        
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
    