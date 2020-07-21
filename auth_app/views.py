from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Login
from .serializers import LoginSerializer, RegistrationSerializer, ErrorMessageSerializer, LoginResponseSerializer
import uuid
from passlib.context import CryptContext
import jwt
import datetime
from school_management.util import roleChecker, roleTimer


pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

#class Based view for login
class LoginView(APIView):
    def post(self, request):
        serializer  = LoginSerializer(data = request.data)
        if serializer.is_valid():
            user = Login.objects.get(email__exact = serializer.data['email'])
            try :
                if pwd_context.verify (serializer.data['password'], user.password):
                    accessToken = jwt.encode({'exp':roleTimer(user.role),'email':user.email, 'role':user.role}, 'secret')
                    return Response(dict(accessToken=accessToken), status= status.HTTP_201_CREATED)
                return Response( dict(code="Failed", message ="Invalid User Name or Password"), status = status.HTTP_401_UNAUTHORIZED)
            except:
                return Response( dict(code="Failed", message ="Invalid User Name or Password"), status = status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)



# Create your views here.
class RegisterView(APIView):
    def post(self, request):
            try:
                authToken = request.headers["auth"]
                payload  = jwt.decode(authToken,"secret")
                role = payload['role']
                serializer  = RegistrationSerializer(data = request.data)
                if serializer.is_valid():
                    if(roleChecker(role,request.data['role'])):
                        loginSerializer = Login(
                                        name = request.data['name'],
                                        email =  request.data['email'],
                                        role = request.data['role'],
                                        image = request.data['image'],
                                        password = pwd_context.encrypt(request.data['password']))
                        ProfileSerializer.save()
                        return Response(status= status.HTTP_201_CREATED)
                    return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)   
                return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
            except jwt.exceptions.ExpiredSignatureError:
                return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)   
            except jwt.exceptions.DecodeError:
                 return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)   
            except:
               return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)   
    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND) 

# class ProfileView(APIView):
#     def put(self, request):
#             try:
#                 authToken = request.headers["auth"]
#                 payload  = jwt.decode(authToken,"secret")
#                 role = payload['role']
#                 serializer  = ProfileSerializer(data = request.data) 
#                  if serializer.is_valid():
#                      user = Register.objects.get(email__exact = serializer.data['email'])
#             try :
#                 if pwd_context.verify (serializer.data['password'], user.password):
#                     accessToken = jwt.encode({'exp':roleTimer(user.role),'email':user.email, 'role':user.role}, 'secret')
#                     return Response(dict(accessToken=accessToken), status= status.HTTP_201_CREATED)
#                 return Response( dict(code="Failed", message ="Invalid User Name or Password"), status = status.HTTP_401_UNAUTHORIZED)
#             except:
#                 return Response( dict(code="Failed", message ="Invalid User Name or Password"), status = status.HTTP_401_UNAUTHORIZED)

#         return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

#     def get(self, request):
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     def put(self, request):
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     def delete(self, request):
#         return Response(status=status.HTTP_404_NOT_FOUND)
