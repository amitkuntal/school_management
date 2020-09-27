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
from django.db.models.functions import Cast
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
            if(role == 'Student'):
                user = Login.objects.get(email__exact = payload['email'])
                student = Student.objects.get(userid__exact = user.id)
                test1 = Test.objects.filter(classid__exact = student.promotedclassid, status__exact = "Published").exclude(id__in=Result.objects.filter(userid__exact = student.userid, status__exact ="Submitted").values_list('testid', flat=True))
                tests = TestSerializer(test1, many = True)
                return Response(tests.data, status=status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthorized access"), status=status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)



class SubjectView(APIView):
    def get(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            userinfo = Login.objects.get(email__exact = payload['email'])
            student = Student.objects.get(userid__exact = userinfo.id)
            subject = SubjectSerializer(Subject.objects.filter(classid__exact = student.promotedclassid), many=True)
            return Response(data =  subject.data, status= status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
       return Response(status=status.HTTP_404_NOT_FOUND)
    
    def delete(self, request):
       return Response(status=status.HTTP_404_NOT_FOUND)



class HomeWorkView(APIView):
    def get(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            userinfo = Login.objects.get(email__exact = payload['email'])
            student = Student.objects.get(userid__exact = userinfo.id)
            homeWork = AddHomeworkSerializer(Homework.objects.filter(classid__exact = student.promotedclassid).order_by('homeworkdate').all(), many = True)
            data = homeWork.data
            return Response(data = data, status= status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class SubmitQuestion(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            userinfo = Login.objects.get(email__exact = payload['email'])
            question = Question.objects.get(id__exact = request.data["id"])
            submission = Submission.objects.get_or_create(userid__exact=userinfo.id, testid__exact=question.testid, questionid__exact = question.id)[0]
            submission.userid = userinfo.id
            submission.testid = question.testid
            submission.questionid = question.id
            submission.submission = request.data["answer"]
            result = Result.objects.get_or_create(userid__exact = userinfo.id, testid__exact = question.testid)[0]
            result.userid = userinfo.id
            result.testid = question.testid
            result.status = "Processing"
            if(question.answer == request.data["answer"]):
                result.score = result.score + int(question.marks)
                submission.mark = int(question.marks)
            else:
                submission.mark = 0 
            submission.save()
            result.save()
            return Response(dict(code="200", message="Success"), status= status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

class GetStudentScore(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            userinfo = Login.objects.get(email__exact = payload['email'])
            result = ResultSerializer(Result.objects.get(userid__exact = userinfo.id, testid__exact = request.data["testid"]))
            return Response(result.data, status= status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status = status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status = status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status = status.HTTP_404_NOT_FOUND)

class SubmitTest(APIView):
    def post(self, request):
        try:
            marks = 0
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            if(payload["role"] == 'Student'):
                userinfo = Login.objects.get(email__exact = payload['email'])
                submissions = Submission.objects.filter(userid__exact = userinfo.id, testid__exact = request.data["testid"]).all()
                for submission in submissions:
                    marks = marks + submission.mark
                result = Result.objects.get_or_create(userid__exact = userinfo.id, testid__exact = request.data["testid"])[0]
                result.userid = userinfo.id
                result.testid = request.data["testid"]
                result.status = "Submitted"
                result.score = marks
                result.save()
                return Response(dict(code="200", message="Your test is submitted. Your score is "+str(result.score)), status= status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthorized"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status = status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status = status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status = status.HTTP_404_NOT_FOUND)


class GetTestsWithResult(APIView):
    def get(self, request):
        try:
            marks = 0
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            if(payload["role"] == 'Student'):
                userinfo = Login.objects.get(email__exact = payload['email'])
                personalInfo = Student.objects.get(userid__exact = userinfo.id)
                tests = TestSerializer(Test.objects.filter(classid__exact = personalInfo.promotedclassid, status__in = ["Expired", "Published"]), many = True)
                tests = tests.data
                for test in tests:
                    checkResultExist = Result.objects.get_or_create(userid__exact = userinfo.id, testid__exact = uuid.UUID(test["id"]))
                    if(checkResultExist[1]):
                        test["result"] = 0               
                    else:
                        marks = checkResultExist[0]
                        test["result"] = marks.score
                    return Response(tests, status= status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthorized"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status = status.HTTP_404_NOT_FOUND)

    def post(self, request):
        return Response(status = status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status = status.HTTP_404_NOT_FOUND)