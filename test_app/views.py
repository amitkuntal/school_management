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
            if(role in ["School", "Teacher"]):
                classid = ""
                if(role == "Teacher"):
                    user = Login.objects.get(email__exact = payload["email"])
                    teacher =  Employee.objects.get(userid__exact = user.id)
                    classid = teacher.classid
                else:
                    classid = request.data["classid"]
                tests = TestSerializer(Test.objects.filter(classid__exact = classid, status__exact = request.data["status"]).all(), many = True)
                tests = tests.data
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
            if(role in ["School", "Teacher"]):
                classid = ""
                if(role == "Teacher"):
                    user = Login.objects.get(email__exact = payload["email"])
                    teacher =  Employee.objects.get(userid__exact = user.id)
                    classid = teacher.classid
                else:
                    classid = request.data["classid"]
                test = Test(classid = classid, testname = request.data["testname"], duration = request.data["duration"], status = request.data["status"], expiredate = request.data["expiredate"])
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
            if(role in ["School", "Teacher", "Student"]):
                questions = QuestionSerializer(Question.objects.filter(testid__exact = request.data["testid"]), many = True)
                questions = questions.data
                return Response(questions, status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

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
                Question.objects.filter(id__exact = request.data["id"]).delete()
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


class QuestionCount(APIView):
    def put(self, request):
        return Response(status= status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status= status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            question = Question.objects.filter(testid__exact = request.data["testid"]).count()
            return Response(dict(count=question), status = status.HTTP_200_OK)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class AllStudentSubmission(APIView):
    def put(self, request):
        return Response(status= status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status= status.HTTP_404_NOT_FOUND)
        
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ["School", "Teacher"]):
                users = UserInfoSerializer(Login.objects.filter(id__in = Student.objects.filter(promotedclassid__exact = request.data["classid"]).values_list('userid',flat= True)), many = True)
                users = users.data
                for user in users:
                    checkResultExist = Result.objects.get_or_create(userid__exact = user["id"], testid__exact = uuid.UUID(request.data["testid"]))
                    if(checkResultExist[1]):
                        user["result"] = 0               
                    else:
                        marks = checkResultExist[0]
                        user["result"] = marks.score
                return Response(users, status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthorized"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)



class StudentSubmissions(APIView):
    def put(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ["School", "Teacher"]):
                score = 0
                submission = Submission.objects.get(questionid__exact = request.data["questionid"], userid = request.data["userid"])
                submission.mark = int(request.data["mark"])
                submission.save()
                submissions = Submission.objects.filter(testid__exact = request.data["testid"], userid__exact = request.data["userid"])
                for sub in submissions:
                    score = score + submission.mark

                result = Result.objects.get(testid__exact = request.data["testid"], userid = request.data["userid"])
                result.score = score
                result.save()
                return Response(dict(code="200", message="Success"), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthorize access"), status= status.HTTP_401_UNAUTHORIZED)
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
                questions =QuestionSerializer(Question.objects.filter(testid__exact = request.data["testid"]), many = True)
                questions = questions.data
                for question in questions:
                    checkResultExist = Submission.objects.get_or_create(questionid__exact = question["id"], userid__exact =request.data["userid"])
                    if(checkResultExist[1]):
                        question["status"] = "Unattempted"             
                    else:
                        submission = checkResultExist[0]
                        question["submission"] = submission.submission
                        if(question["answer"] == submission.submission):
                            question["status"] = "Correct"
                        else:
                            question["status"] = "Wrong"
                return Response(questions, status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthorize access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
