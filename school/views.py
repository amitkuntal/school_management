from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from auth_app.models import *
import jwt


class RegisterStudentView(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            serializer  = RegistrationSerializer(data = request.data['profile'])
            schoolid = ''
            if(role=='School'):
                school = Login.objects.get(email__exact = payload['email'])
                schoolid = school.id
            elif(role in ['Teacher','Accountant','Reception']):
                user  = Login.objects.get(email__exact = payload['email'])
                employee = Employee.objects.get(userid__exact = user.id)
                schoolid = employee.schoolid
            if serializer.is_valid():
                if(roleChecker(role,request.data['role'])):
                    loginSerializer = Login(
                                    name = request.data['name'],
                                    email =  request.data['email'],
                                    role = request.data['role'],
                                    image = request.data['image'],
                                    password = pwd_context.encrypt(request.data['password']))
                    loginSerializer.save()
                    student = StudentSerializer(data = request.data['additionalInfo'])
                    data = request.data['additionalInfo']
                    if(student.is_valid):
                        studentSerializer = Student(
                                            userid = loginSerializer.id, 
                                            address1 = data['address1'],
                                            address2 = data['address2'],
                                            address3 = data['address3'],
                                            city = data['city'],
                                            state = data['state'],
                                            zip = data['zip'],
                                            schoolid = schoolid,
                                            classid = data['classid'],
                                            fathername = data['fathername'],
                                            mothername = data['mothername'],
                                            mobileno1= data['mobileno1'],
                                            mobileno2=data['mobileno2'],
                                            addmissiondate = data['addmissiondate'],
                                            srno=data['srno'],
                                            promotedclassid = data['promotedclassid'])
                        studentSerializer.save()
                        return Response(status= status.HTTP_201_CREATED)
                    return Response(student.errors, status= status.HTTP_400_BAD_REQUEST)
                return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterClassView(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            schoolid = ''
            if(role=='School'):
                school = Login.objects.get(email__exact = payload['email'])
                schoolid = school.id
            elif(role in ['Teacher','Accountant','Reception']):
                user  = Login.objects.get(email__exact = payload['email'])
                employee = Employee.objects.get(userid__exact = user.id)
                schoolid = employee.schoolid
            request.data['schoolid'] = str(schoolid)
            serializer  = ClassSerializer(data = request.data)
            if serializer.is_valid():
                if(role in ['Teacher', 'Accountant', 'Reception', 'School']):
                    print(schoolid)
                    classSerializer = Class(
                                    schoolid = schoolid,
                                    classname = request.data['classname'],
                                    section = request.data['section'])
                    classSerializer.save()
                    return Response(status= status.HTTP_201_CREATED)
                return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            schoolid = ''
            if(role=='School'):
                school = Login.objects.get(email__exact = payload['email'])
                schoolid = school.id
            elif(role in ['Teacher','Accountant','Reception']):
                user  = Login.objects.get(email__exact = payload['email'])
                employee = Employee.objects.get(userid__exact = user.id)
                schoolid = employee.schoolid
            if(role in ['Teacher', 'Accountant', 'Reception', 'School']):
                classSerializer = ClassSerializer(Class.objects.filter(schoolid = str(schoolid)).all(), many=True)
                return Response(classSerializer.data,status= status.HTTP_201_CREATED)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

