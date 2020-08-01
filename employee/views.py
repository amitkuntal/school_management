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


# class AllEmployee(APIView):
#     def post(self, request):
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     def put(self, request):
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     def get(self, request):
#         try:
#             authToken = request.headers["auth"]
#             payload  = jwt.decode(authToken,"secret")
#             role = payload['role']
#             if (role == 'School'):
#                 user = Login.objects.get(email__exact = payload['email'])
#                 userid =  user.id
#                 employee = EmployeeSerializer(Employee.objects.filter(schoolid__exact = userid), many =True)
#                 employeeids = []
#                 for x in employee.data:
#                     employeeids.append(x['userid'])
#                 login =  Login.objects.filter()

#             return Response(dict(code="401", message="Unauthrized"),status=status.HTTP_401_UNAUTHORIZED)
#         except jwt.exceptions.ExpiredSignatureError:
#             return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
#         except jwt.exceptions.DecodeError:
#                 return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
#         except:
#             return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)

#     def delete(self, request):
#         return Response(status=status.HTTP_404_NOT_FOUND)







