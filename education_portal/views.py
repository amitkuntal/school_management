from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from auth_app.models import *
import jwt


class TestView(APIView):
    def post(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            school = Login.objects.filter(role='Admin').all()
            student = Login.objects.filter(role= 'Student').all()
            employee = Login.objects.filter(role__in = ['Teacher','Accountant','Reception'])
            return Response(dict(school=len(school), student = len(student), employee = len(employee)),status=status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
