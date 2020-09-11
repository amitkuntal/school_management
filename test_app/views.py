from django.shortcuts import render
from rest_framework.parsers import JSONParser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.http import HttpResponse, JsonResponse
from auth_app.models import *
from auth_app.serializers import *
from school_management.util import *
import jwt
import openpyxl

# Create your views here.

class Tests(APIView):
    def put(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            schoolid = ''
            if(role in ["School", "Teacher"]):
                classid = ""
                if(role == "Teacher"):
                    user = Login.objects.get(email__exact = payload["email"])
                    teacher =  Employee.objects.get(userid__exact = user.id)
                    classid = teacher.classid
                else:
                    classid = request.data["classid"]
                tests = TestSerializer(Test.objects.filter(classid__exact = classid).all(), many = True)
                tests = tests.data
                for test in tests:
                    subject = Subject.objects.get(id__exact = test["subjectid"])
                    test["subjectName"] = subject.subjectname
                return Response(tests, status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response(status= status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            schoolid = ''
            if(role in ["School", "Teacher"]):
                classid = ""
                if(role == "Teacher"):
                    user = Login.objects.get(email__exact = payload["email"])
                    teacher =  Employee.objects.get(userid__exact = user.id)
                    classid = teacher.classid
                else:
                    classid = request.data["classid"]
                test = Test(classid = classid, subjectid = request.data["subjectid"], testname = request.data["testname"], duration = request.data["duration"], status = request.data["status"], expiredate = request.data["expiredate"])
                test.save()
                return Response(dict(code = "200", message = "Success"), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class TestUpdate(APIView):
    def put(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ["School", "Teacher"]):
                Question.objects.filter(testid__exact = request.data["testid"]).delete()
                Test.objects.filter(id__exact = request.data["testid"]).delete()
                Result.objects.filter(testid__exact = request.data["testid"]).delete()
                return Response(dict(code="200", message="Success"), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response(status= status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ["School", "Teacher"]):
                test = Test.objects.get(id__exact = request.data["testid"])
                test.status = request.data["status"]
                test.testname = request.data["testname"]
                test.expiredate = request.data["expiredate"]
                test.save()
                return Response(dict(code = "200", message = "Success"), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class Questions(APIView):
    def put(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ["School", "Teacher"]):
                test = Test.objects.get(id__exact = request.data["testid"])
                test = test.data
                questions = QuestionSerializer(Question.objects.filter(testid__exact = request.data["testid"]), many = True)
                questions = questions.data
                test["questions"] = questions
                return Response(test, status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response(status= status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ["School", "Teacher"]):
                question = Question(testid = request.data["testid"],
                 question = request.data["question"],
                 questiontype = request.data["questiontype"],
                 option1=request.data["option1"],
                 option2=request.data["option2"],
                 option3=request.data["option3"],
                 option4=request.data["option4"],
                 marks = request.data["marks"],
                 answer = request.data["answer"]
                  )
                question.save()
                return Response(dict(code = "200", message = "Success"), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class QuestionUpdate(APIView):
    def put(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ["School", "Teacher"]):
                Question.objects.get(id__exact = request.data["id"]).delete()
                return Response(test, status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def get(self, request):
        return Response(status= status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ["School", "Teacher"]):
                question = Question.objects.get(id__exact = request.data["id"])
                question.question = request.data["question"],
                question.questiontype = request.data["questiontype"],
                question.option1=request.data["option1"],
                question.option2=request.data["option2"],
                question.option3=request.data["option3"],
                question.option4=request.data["option4"],
                question.marks = request.data["marks"],
                question.answer = request.data["answer"]
                question.save()
                return Response(dict(code = "200", message = "Success"), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
