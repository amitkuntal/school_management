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


class RegisterStudentView(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            schoolid = ''
            classid = ''
            if(role in ['Teacher','Accountant','Reception']):
                user  = Login.objects.get(email__exact = payload['email'])
                employee = Employee.objects.get(userid__exact = user.id)
                schoolid = employee.schoolid
                classid = employee.classid
            if(roleChecker(role,request.data['role'])):
                loginSerializer = RegistrationSerializer(data=dict(
                                name = request.data['name'],
                                email =  request.data['email'],
                                role = request.data['role'],
                                image = request.data['image'],
                                password = pwd_context.encrypt(request.data['password'])))
                if(loginSerializer.is_valid()):
                    login  = Login(
                                name = request.data['name'],
                                email =  request.data['email'],
                                role = request.data['role'],
                                image = request.data['image'],
                                password = pwd_context.encrypt(request.data['password']))
                    studentSerializer = StudentSerializer(
                                        data = dict(
                                        userid = login.id, 
                                        address1 = request.data['address1'],
                                        address2 = request.data['address2'],
                                        address3 = request.data['address3'],
                                        city = request.data['city'],
                                        state = request.data['state'],
                                        zip = request.data['zip'],
                                        schoolid = str(schoolid),
                                        dob =  request.data['dob'],
                                        classid = classid,
                                        fathername = request.data['fathername'],
                                        mothername = request.data['mothername'],
                                        mobileno1= request.data['mobileno1'],
                                        mobileno2=request.data['mobileno2'],
                                        admissiondate = request.data['addmissiondate'],
                                        srno=request.data['srno'],
                                        promotedclassid = classid))
                    if studentSerializer.is_valid():
                        login.save()
                        student = Student(
                                        userid = login.id, 
                                        address1 = request.data['address1'],
                                        address2 = request.data['address2'],
                                        address3 = request.data['address3'],
                                        city = request.data['city'],
                                        state = request.data['state'],
                                        zip = request.data['zip'],
                                        schoolid = str(schoolid),
                                        dob =  request.data['dob'],
                                        classid = classid,
                                        fathername = request.data['fathername'],
                                        mothername = request.data['mothername'],
                                        mobileno1= request.data['mobileno1'],
                                        mobileno2=request.data['mobileno2'],
                                        admissiondate = request.data['addmissiondate'],
                                        srno=request.data['srno'],
                                        promotedclassid = classid
                                        )
                        student.save()
                        return Response(dict(code="200", message="Succesfully created"),status= status.HTTP_201_CREATED)
                    return Response(studentSerializer.errors,  status= status.HTTP_401_UNAUTHORIZED)
                return Response(loginSerializer.errors,  status= status.HTTP_401_UNAUTHORIZED)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            classid = ''
            if(role in ['Teacher','Accountant','Reception']):
                user  = Login.objects.get(email__exact = payload['email'])
                employee = Employee.objects.get(userid__exact = user.id)
                classid = employee.classid
                student = Student.objects.filter(promotedclassid__exact = classid).all()
                studentids = []
                for x in student:
                    studentids.append(x.userid)
                users =  Login.objects.filter(id__in = studentids).all()
                userSerializer = UserSerializer(users, many = True)
                userdata =  userSerializer.data
                for user in userdata:
                    user['image'] = readFiles(user['image'])
                return Response(userdata, status= status.HTTP_201_CREATED)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
            return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except Student.DoesNotExist:
            return Response(dict(code="400", message="Students not found"), status= status.HTTP_401_UNAUTHORIZED)
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
            if(role in ['Teacher', 'Accountant', 'Reception']):
                userinfo = Login.objects.get(email__exact = payload['email'])
                employee = Employee.objects.get(userid__exact = userinfo.id)
                subject = SubjectSerializer(Subject.objects.filter(classid__exact = employee.classid), many=True)
                return Response(data =  subject.data, status= status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ['Teacher', 'Accountant', 'Reception']):
                userinfo = Login.objects.get(email__exact = payload["email"])
                employeeInfo = Employee.objects.get(userid__exact = userinfo.id)
                subjectAdd = Subject(classid = employeeInfo.classid, subjectname = request.data["subjectname"])
                subjectAdd.save()
                return Response(dict(code="200", message="Succesfully created"),status= status.HTTP_201_CREATED)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)


class HomeWorkView(APIView):
    def get(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ['Teacher', 'Accountant', 'Reception']):
                userinfo = Login.objects.get(email__exact = payload['email'])
                employee = Employee.objects.get(userid__exact = userinfo.id)
                homeWork = AddHomeworkSerializer(Homework.objects.filter(classid__exact = employee.classid).order_by('homeworkdate').all(), many = True)
                data = homeWork.data
                for x in data:
                    if x["image"] != '/media/null':
                        x["image"] = readFiles(x["image"])
                return Response(data = data, status= status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            data  = request.data
            if(role in ['Teacher', 'Accountant', 'Reception']):
                userinfo = Login.objects.get(email__exact = payload["email"])
                employeeInfo = Employee.objects.get(userid__exact = userinfo.id)
                homework = Homework.objects.filter(classid__exact = employeeInfo.classid, homeworkdate__exact = request.data["homeworkdate"]).get_or_create()[0]
                homework.homework = request.data["homework"]
                homework.homeworkdate =request.data["homeworkdate"]
                homework.teacherid = employeeInfo.userid
                homework.classid = employeeInfo.classid
                homework.image  = request.data["image"]
                homework.save()
                return Response(dict(code="200", message="Succesfully created"),status= status.HTTP_201_CREATED)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)




