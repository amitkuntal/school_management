from rest_framework import serializers
from .models import School, Admin, Student, Class ,FeeStructure, Homework, Attendance, FeeDeposit, TransferCertificate
class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ['userid', 'schoolname', 'address1', 'address2' , 'address3', 'city', 'state', 'zip']

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admin
        fields = ['userid', 'mobile', 'address2']

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