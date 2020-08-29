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


class StudentAttendanceView(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ['Teacher','Accountant', 'Reception']):
                studentinfo = Student.objects.get(userid__exact = request.data["id"])
                studentAttendance =  Attendance.objects.get_or_create(userid__exact = request.data['id'], attendancedate__exact = request.data['date'])[0]
                studentAttendance.status = request.data["status"]
                studentAttendance.userid = request.data["id"]
                studentAttendance.attendancedate = request.data["date"]
                studentAttendance.classid = studentinfo.promotedclassid
                studentAttendance.schoolid = studentinfo.schoolid
                studentAttendance.save()
                return Response(dict(code="200", message="Success"), status= status.HTTP_200_OK)
            return Response(dict(code="401", message="Unauthorized"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ['Teacher','Accountant', 'Reception']):
                teacherinfo = Login.objects.get(email__exact = payload['email'])
                employeeinfo = Employee.objects.get(userid__exact = teacherinfo.id)
                schoolid = employeeinfo.schoolid
                classid = employeeinfo.classid

                students = Student.objects.filter(promotedclassid__exact = classid).all()
                studentsids = []
                for x in students:
                    studentsids.append(x.userid)
                users =  Login.objects.filter(id__in = studentsids).all()
                data = UserSerializer(users, many = True).data
                for user in data:
                    studentAttendance = AttendanceSerializer(Attendance.objects.filter(userid__exact = user["id"],attendancedate__range=[request.data["fromDate"], request.data["toDate"]]).order_by('attendancedate').all(),many=True)
                    user["attendancedata"] = studentAttendance.data
                return Response(data, status= status.HTTP_200_OK)
            return Response(dict(code="401", message="Unauthorized"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)
    
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


class EmployeeAttendanceView(APIView):
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role == 'School'):
                employeeAttendanceinfo =  EmployeeAttendance.objects.get_or_create(userid__exact = request.data['id'], attendancedate__exact = request.data['date'])[0]
                employeeAttendanceinfo.status = request.data["status"]
                employeeAttendanceinfo.userid = request.data["id"]
                employeeAttendanceinfo.attendancedate = request.data["date"]
                employeeAttendanceinfo.save()
                return Response(dict(code="200", message="Success"), status= status.HTTP_200_OK)
            return Response(dict(code="401", message="Unauthorized"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role == 'School'):
                school = Login.objects.get(email__exact = payload['email'])
                schoolid = school.id
                employee = Employee.objects.filter(schoolid__exact = schoolid).all()
                employeeids = []
                for x in employee:
                    employeeids.append(x.userid)
                users =  Login.objects.filter(id__in = employeeids).all()
                data = UserSerializer(users, many = True).data
                for user in data:
                    user['image'] = readFiles(user['image'])
                    employeeattendance = EmployeeAttendanceSerializer(EmployeeAttendance.objects.filter(userid__exact = user["id"],attendancedate__range=[request.data["fromDate"], request.data["toDate"]]).order_by('attendancedate').all(),many=True)
                    user["attendancedata"] = employeeattendance.data
                return Response(data, status= status.HTTP_200_OK)
            return Response(dict(code="401", message="Unauthorized"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)
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




class StudentSelftAttendanceView(APIView):

    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            studentinfo = UserSerializer(Login.objects.get(email__exact = payload['email']))
            user = studentinfo.data
            studentAttendance = AttendanceSerializer(Attendance.objects.filter(userid__exact = user["id"],attendancedate__range=[request.data["fromDate"], request.data["toDate"]]).order_by('attendancedate').all(),many=True)
            user["attendancedata"] = studentAttendance.data
            return Response(user, status= status.HTTP_200_OK)
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



class StudentAttendanceViewForSchool(APIView):
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role=='School'):
                schoolinfo = Login.objects.get(email__exact = payload['email'])
                students = Student.objects.filter(promotedclassid__exact = request.data["classid"]).all()
                studentsids = []
                for x in students:
                    studentsids.append(x.userid)
                users =  Login.objects.filter(id__in = studentsids).all()
                data = UserSerializer(users, many = True).data
                for user in data:
                    studentAttendance = AttendanceSerializer(Attendance.objects.filter(userid__exact = user["id"],attendancedate__range=[request.data["fromDate"], request.data["toDate"]]).order_by('attendancedate').all(),many=True)
                    user["attendancedata"] = studentAttendance.data
                return Response(data, status= status.HTTP_200_OK)
            return Response(dict(code="401", message="Unauthorized"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Missing Token"), status= status.HTTP_401_UNAUTHORIZED)
    
    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
