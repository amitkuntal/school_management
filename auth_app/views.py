from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from .models import Login,ErrorMessage
from .serializers import LoginSerializer, RegistrationSerializer, ErrorMessageSerializer
import uuid
from passlib.context import CryptContext

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
            serializer.save()
            return Response(serializer.data, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)



# Create your views here.

@api_view(['POST'])
def register(request):
    serializer  = RegistrationSerializer(data = request.data)
    if serializer.is_valid():
        loginSerializer = Login(
                                name = request.data['name'],
                                email =  request.data['email'],
                                role = request.data['role'],
                                image = request.data['image'],
                                password = pwd_context.encrypt(request.data['password']))
        loginSerializer.save()
        return Response(status= status.HTTP_201_CREATED)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

