from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from auth_app.models import *
from auth_app.serializers import *
import jwt


class RegisterFeeView(APIView):
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
            serializer  = FeeStructureSerializer(data = request.data)
            if serializer.is_valid():
                if(role in ['Teacher', 'Accountant', 'Reception', 'School']):
                    print(schoolid)
                    feeSerializer = FeeStructure(
                                    classid = request.data['classid'],
                                    schoolid = schoolid,
                                    classname = request.data['classname'],
                                    section = request.data['section'])
                    feeSerializer.save()
                    return Response(status= status.HTTP_201_CREATED)
                return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

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
                feeSerializer = FeeStructureSerializer(FeeStructure.objects.filter(schoolid = str(schoolid)).all(), many=True)
                return Response(feeSerializer.data,status= status.HTTP_201_CREATED)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)




class GetFeeStructureByClassid(APIView):
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, clasid='employee'):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ['Teacher','Accountant','Reception']):
                user  = Login.objects.get(email__exact = payload['email'])
                employee = Employee.objects.get(userid__exact = user.id)
                clasid = employee.classid
            if(role in ['Teacher', 'Accountant', 'Reception', 'School']):
                feeSerializer = FeeStructureSerializer(FeeStructure.objects.get(classid__exact = str(classid)))
                return Response(feeSerializer.data,status= status.HTTP_201_CREATED)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)


    def post(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
