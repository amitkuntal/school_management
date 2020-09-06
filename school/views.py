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


class RegisterStudentView(APIView):
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
            if(roleChecker(role,request.data['role'])):
                loginSerializer = RegistrationSerializer(data=dict(
                                name = request.data['name'],
                                email =  request.data['email'],
                                role = request.data['role'],
                                image = request.data['image'].file.read(),
                                password = request.data['password']))
                if(loginSerializer.is_valid()):
                    login  = Login(
                                name = request.data['name'],
                                email =  request.data['email'],
                                role = request.data['role'],
                                image = resizeImage(request.data['image']),
                                password = request.data['password'])
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
                                        classid = request.data['classid'],
                                        fathername = request.data['fathername'],
                                        mothername = request.data['mothername'],
                                        mobileno1= request.data['mobileno1'],
                                        mobileno2=request.data['mobileno2'],
                                        admissiondate = request.data['addmissiondate'],
                                        srno=request.data['srno'],
                                        promotedclassid = request.data['promotedclassid']))
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
                                        classid = request.data['classid'],
                                        fathername = request.data['fathername'],
                                        mothername = request.data['mothername'],
                                        mobileno1= request.data['mobileno1'],
                                        mobileno2=request.data['mobileno2'],
                                        admissiondate = request.data['addmissiondate'],
                                        srno=request.data['srno'],
                                        promotedclassid = request.data['promotedclassid']
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
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterClassView(APIView):
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
            serializer  = ClassSerializer(data = request.data)
            if serializer.is_valid():
                if(role in ['Teacher', 'Accountant', 'Reception', 'School']):
                    print(schoolid)
                    classSerializer = Class(
                                    schoolid = schoolid,
                                    classname = request.data['classname'],
                                    section = request.data['section'])
                    classSerializer.save()
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
                classSerializer = ClassSerializer(Class.objects.filter(schoolid = str(schoolid)).all(), many=True)
                data  =  classSerializer.data
                for x in data:
                    try:
                        employee =  Employee.objects.filter(classid = x["id"]).all()
                        x["teacherCount"] = len(employee)
                    except:
                        x["teacherCount"] = 0

                for x in data:
                    try:
                        student =  Student.objects.filter(promotedclassid = x["id"]).all()
                        x["studentCount"] = len(student)
                    except Student.DoesNotExist:
                        x["studentCount"] = 0
                return Response(data,status= status.HTTP_201_CREATED)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetAllStudentFromClass(APIView):
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
            if(role in ['Teacher', 'Accountant', 'Reception', 'School']):
                student = Student.objects.filter(promotedclassid__exact = request.data['classid']).all()
                studentids = []
                for x in student:
                    studentids.append(x.userid)
                users =  Login.objects.filter(id__in = studentids).all()
                userSerializer = UserSerializer(users, many = True)
                userdata =  userSerializer.data
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

    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        return Response(status= status.HTTP_404_NOT_FOUND)
    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class RegisterEmployeeView(APIView):
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
            if(roleChecker(role,request.data['role'])):
                loginSerializer = RegistrationSerializer(data=dict(
                                name = request.data['name'],
                                email =  request.data['email'],
                                role = request.data['role'],
                                image = request.data['image'].file.read(),
                                password = request.data['password']))
                if(loginSerializer.is_valid()):
                    login  = Login(
                                name = request.data['name'],
                                email = request.data['email'],
                                role = request.data['role'],
                                image = resizeImage(request.data['image']),
                                password = request.data['password'])
                    employeeSerializer = EmployeeSerializer(
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
                                        classid = request.data['classid'],
                                        fathername = request.data['fathername'],
                                        mothername = request.data['mothername'],
                                        mobile = request.data['mobile'],
                                        salary=request.data['salary'],
                                        dateOfJoining = request.data['dateOfJoining']))
                    if employeeSerializer.is_valid():
                        login.save()
                        employee = Employee(userid = login.id, 
                                        address1 = request.data['address1'],
                                        address2 = request.data['address2'],
                                        address3 = request.data['address3'],
                                        city = request.data['city'],
                                        state = request.data['state'],
                                        zip = request.data['zip'],
                                        schoolid = str(schoolid),
                                        dob =  request.data['dob'],
                                        classid = request.data['classid'],
                                        fathername = request.data['fathername'],
                                        mothername = request.data['mothername'],
                                        mobile= request.data['mobile'],
                                        salary=request.data['salary'],
                                        dateOfJoining = request.data['dateOfJoining'])
                        employee.save()
                        return Response(dict(code="200", message="Succesfully created"),status= status.HTTP_201_CREATED)
                    return Response(employeeSerializer.errors,  status= status.HTTP_401_UNAUTHORIZED)
                return Response(loginSerializer.errors,  status= status.HTTP_401_UNAUTHORIZED)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
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
                employee = Employee.objects.filter(schoolid__exact = schoolid).all()
                employeeids = []
                for x in employee:
                    employeeids.append(x.userid)
                users =  Login.objects.filter(id__in = employeeids).all()
                data = UserSerializer(users, many = True).data
                return Response(data,status= status.HTTP_201_CREATED)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
            return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except Employee.DoesNotExist:
            return Response(dict(code="400", message="Employee not found"), status= status.HTTP_401_UNAUTHORIZED)
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
            schoolid = ''
            if(role=='School'):
                school = Login.objects.get(email__exact = payload['email'])
                schoolid = school.id
                classes =  ClassSerializer(Class.objects.filter(schoolid__exact = schoolid).all(), many=True)
                data =  classes.data
                for x in data:
                    subjects = SubjectSerializer(Subject.objects.filter(classid__exact = x["id"]), many=True)
                    x["subjects"] = subjects.data
                return Response(data =  data, status= status.HTTP_200_OK)
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
            if(role in ['Teacher', 'Accountant', 'Reception', 'School']):
                addSubjectSerializer =  AddSubjectSerializer(data = request.data)
                if(addSubjectSerializer.is_valid()):
                    addSubjectSerializer.save()
                    return Response(dict(code="200", message="Succesfully created"),status= status.HTTP_201_CREATED)
                return Response(addSubjectSerializer.errors,  status= status.HTTP_401_UNAUTHORIZED)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)





class ClassSubjectView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role == 'School'):
                subject = SubjectSerializer(Subject.objects.filter(classid__exact=request.data["classid"]), many= True)
                return Response(subject.data, status= status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class AddSchoolEducationView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ['School', 'Reception','Teacher', 'Accountant']):
                video = AddEducationPortal(data =  request.data)
                if(video.is_valid()):
                    video.save()
                    return Response(dict(code="200", message="Video Added"), status = status.HTTP_200_OK)
                return Response(video.errors, status= status.HTTP_400_BAD_REQUEST)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetSchoolEducationView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ['School', 'Reception','Teacher', 'Accountant', 'Student']):
                video = EducationPortalSerializer(EducationPortal.objects.filter(subjectid__exact = request.data['subjectid']), many=True)
                return Response(video.data, status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class TimeTableView(APIView):
    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role =='School' ):
                mondayTimeTable = TimeTableSerializer(TimeTable.objects.filter(classid__exact = request.data["classid"], day__exact = "Monday").order_by('period').all(), many=True)
                mondayTimeTable = mondayTimeTable.data
                for x in mondayTimeTable:
                    teacherinfo = Login.objects.get(id__exact= x["teacherid"])
                    x["teachername"] = teacherinfo.name
                    subjectinfo = Subject.objects.get(id__exact = x["subjectid"])
                    x["subjectname"] = subjectinfo.subjectname
                
                tuesdayTimeTable = TimeTableSerializer(TimeTable.objects.filter(classid__exact = request.data["classid"], day__exact = "Tuesday").order_by('period').all(), many=True)
                tuesdayTimeTable = tuesdayTimeTable.data
                for x in tuesdayTimeTable:
                    teacherinfo = Login.objects.get(id__exact= x["teacherid"])
                    x["teachername"] = teacherinfo.name
                    subjectinfo = Subject.objects.get(id__exact = x["subjectid"])
                    x["subjectname"] = subjectinfo.subjectname

                wednesdayTimeTable = TimeTableSerializer(TimeTable.objects.filter(classid__exact = request.data["classid"], day__exact = "Wednesday").order_by('period').all(), many=True)
                wednesdayTimeTable = wednesdayTimeTable.data
                for x in wednesdayTimeTable:
                    teacherinfo = Login.objects.get(id__exact= x["teacherid"])
                    x["teachername"] = teacherinfo.name
                    subjectinfo = Subject.objects.get(id__exact = x["subjectid"])
                    x["subjectname"] = subjectinfo.subjectname
                
                thursdayTimeTable = TimeTableSerializer(TimeTable.objects.filter(classid__exact = request.data["classid"], day__exact = "Thursday").order_by('period').all(), many=True)
                thursdayTimeTable = thursdayTimeTable.data
                for x in wednesdayTimeTable:
                    teacherinfo = Login.objects.get(id__exact= x["teacherid"])
                    x["teachername"] = teacherinfo.name
                    subjectinfo = Subject.objects.get(id__exact = x["subjectid"])
                    x["subjectname"] = subjectinfo.subjectname

                fridayTimeTable = TimeTableSerializer(TimeTable.objects.filter(classid__exact = request.data["classid"], day__exact = "Friday").order_by('period').all(), many=True)
                fridayTimeTable = fridayTimeTable.data
                for x in wednesdayTimeTable:
                    teacherinfo = Login.objects.get(id__exact= x["teacherid"])
                    x["teachername"] = teacherinfo.name
                    subjectinfo = Subject.objects.get(id__exact = x["subjectid"])
                    x["subjectname"] = subjectinfo.subjectname

                saturdayTimeTable = TimeTableSerializer(TimeTable.objects.filter(classid__exact = request.data["classid"], day__exact = "Saturday").order_by('period').all(), many=True)
                saturdayTimeTable = saturdayTimeTable.data
                for x in wednesdayTimeTable:
                    teacherinfo = Login.objects.get(id__exact= x["teacherid"])
                    x["teachername"] = teacherinfo.name
                    subjectinfo = Subject.objects.get(id__exact = x["subjectid"])
                    x["subjectname"] = subjectinfo.subjectname

                    
                return Response(dict(monday=mondayTimeTable, tuesday=tuesdayTimeTable,
                                     wednesday = wednesdayTimeTable,
                                     thursday = thursdayTimeTable,
                                     friday = fridayTimeTable,
                                     saturday = saturdayTimeTable), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)
        
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role =='School' ):
                schoolinfo = Login.objects.get(email__exact = payload['email'])
                schoolid =  schoolinfo.id
                timetable = TimeTable.objects.filter(schoolid__exact = schoolid, classid__exact = request.data["classid"], day__exact = request.data["day"], period__exact = request.data["period"]).get_or_create()[0]
                timetable.schoolid = schoolid
                timetable.classid = request.data["classid"]
                timetable.day = request.data["day"]
                timetable.period =  request.data["period"]
                timetable.teacherid = request.data["teacherid"]
                timetable.subjectid = request.data["subjectid"]
                timetable.save()
                return Response(dict(code="200", message="Success"), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class GetStudentProfile(APIView):
    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ['School','Reception','Teacher','Accountant'] ):
                userinfo = Login.objects.get_or_create(id__exact =  request.data["userid"])[0]
                userinfo.name = request.data["name"]
                userinfo.email = request.data["email"]
                studentinfo = Student.objects.get_or_create(userid__exact = request.data["userid"])[0]
                studentinfo.dob  =  request.data["dob"]
                studentinfo.fathername = request.data["fathername"]
                studentinfo.mothername = request.data["mothername"]
                studentinfo.mobileno1 = request.data["mobileno1"]
                studentinfo.mobileno2 = request.data["mobileno2"]
                studentinfo.address1 = request.data["address1"]
                studentinfo.address2 = request.data["address2"]
                studentinfo.address3 = request.data["address3"]
                studentinfo.city  = request.data["city"]
                studentinfo.state =  request.data["state"]
                studentinfo.zip = request.data["zip"]
                studentinfo.addmissiondate = request.data["addmissiondate"]
                studentinfo.srno = request.data["srno"]
                studentinfo.promotedclassid  = request.data["promotedclassid"]
                userinfo.save()
                studentinfo.save()
                return Response(dict(code="200", message="Success"), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)
        
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            schoolid = ''
            if(role =='school'):
                schoolinfo = Login.objects.get(email__exact = payload["email"])
                schoolid = schoolinfo.id

            if(role in ['Reception', 'Teacher', 'Accountant']):
                employeinfo  = Login.objects.get(email__exact = payload['email'])
                additionalinfo = Employee.objects.get(userid__exact = employeinfo.id)
                schoolid = additionalinfo.schoolid
            if(role in ['School','Reception','Teacher','Accountant']):
                userinfo = UserSerializer(Login.objects.get(id__exact = request.data["id"]))
                studentinfo = StudentSerializer(Student.objects.get(userid__exact = request.data["id"]))
                userinfo = userinfo.data
                studentinfo = studentinfo.data
                studentclass =  Class.objects.get(id__exact = studentinfo["promotedclassid"])
                studentinfo["currentclass"] = studentclass.classname
                classinfo =  ClassSerializer(Class.objects.filter(schoolid__exact = schoolid).all(), many=True)
                return Response(dict(studentinfo  = studentinfo , userinfo = userinfo, classes = classinfo.data), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

class GetEmployeeProfile(APIView):
    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def put(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ['School','Reception','Teacher','Accountant'] ):
                userinfo = Login.objects.get_or_create(id__exact =  request.data["userid"])[0]
                userinfo.name = request.data["name"]
                userinfo.email = request.data["email"]
                employeeinfo = Employee.objects.get_or_create(userid__exact = request.data["userid"])[0]
                employeeinfo.dob  =  request.data["dob"]
                employeeinfo.fathername = request.data["fathername"]
                employeeinfo.mothername = request.data["mothername"]
                employeeinfo.mobile = request.data["mobile"]
                employeeinfo.address1 = request.data["address1"]
                employeeinfo.address2 = request.data["address2"]
                employeeinfo.address3 = request.data["address3"]
                employeeinfo.city  = request.data["city"]
                employeeinfo.state =  request.data["state"]
                employeeinfo.zip = request.data["zip"]
                employeeinfo.dateOfJoining = request.data["dateOfJoining"]
                employeeinfo.salary = request.data["salary"]
                employeeinfo.classid  = request.data["classid"]
                userinfo.save()
                employeeinfo.save()
                return Response(dict(code="200", message="Success"), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)
        
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            schoolid = ''
            if(role =='School'):
                schoolinfo = Login.objects.get(email__exact = payload["email"])
                schoolid = schoolinfo.id
                userinfo = UserSerializer(Login.objects.get(id__exact = request.data["id"]))
                employeedata = EmployeeSerializer(Employee.objects.get(userid__exact = request.data["id"]))
                userinfo = userinfo.data
                employeedata = employeedata.data
                employeeclass =  Class.objects.get(id__exact = employeedata["classid"])
                employeedata["currentclass"] = employeeclass.classname
                classinfo =  ClassSerializer(Class.objects.filter(schoolid__exact = schoolid).all(), many=True)
                return Response(dict(employeinfo  = employeedata , userinfo = userinfo, classes = classinfo.data), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)



class SchoolProfile(APIView):
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role in ['School'] ):
                schoolinfo = Login.objects.get(email__exact = payload["email"])
                schoolAdditionalInfo = School.objects.get_or_create(userid__exact = schoolinfo.id)[0]
                studentCount = len(Student.objects.filter(schoolid__exact = schoolinfo.id).all())
                teacherCount = len(Employee.objects.filter(schoolid__exact = schoolinfo.id).all())
                return Response(dict(school=UserSerializer(schoolinfo).data, schoolinfo=SchoolSerializer(schoolAdditionalInfo).data, studentcount = studentCount, employeecount= teacherCount), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)
        
    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            schoolid = ''
            if(role =='school'):
                schoolinfo = Login.objects.get(email__exact = payload["email"])
                schoolid = schoolinfo.id

            if(role in ['Reception', 'Teacher', 'Accountant']):
                employeinfo  = Login.objects.get(email__exact = payload['email'])
                additionalinfo = Employee.objects.get(userid__exact = employeinfo.id)
                schoolid = additionalinfo.schoolid
            if(role in ['School','Reception','Teacher','Accountant']):
                userinfo = UserSerializer(Login.objects.get(id__exact = request.data["id"]))
                studentinfo = StudentSerializer(Student.objects.get(userid__exact = request.data["id"]))
                userinfo = userinfo.data
                userinfo["image"] = readFiles(userinfo["image"])
                studentinfo = studentinfo.data
                studentclass =  Class.objects.get(id__exact = studentinfo["promotedclassid"])
                studentinfo["currentclass"] = studentclass.classname
                classinfo =  ClassSerializer(Class.objects.filter(schoolid__exact = schoolid).all(), many=True)
                return Response(dict(studentinfo  = studentinfo , userinfo = userinfo, classes = classinfo.data), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)


class UploadExcel(APIView):
    def put(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)
    def get(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            authToken = request.headers["auth"]
            payload  = jwt.decode(authToken,"secret")
            role = payload['role']
            if(role =='School'):
                excel_file = request.FILES["file"]
                wb = openpyxl.load_workbook(excel_file)
                worksheet = wb["Sheet1"]
                for row in worksheet.iter_rows():
                    link = row[1].value
                    link = link.split("v=")[1]
                    link = link.split("&")[0]
                    link = "https://www.youtube.com/embed/"+link
                    tutorial = EducationPortal(subjectid = request.data["subjectid"], chaptername=row[0].value, videolink=link)
                    tutorial.save()
                return Response(dict(code="200", message="pass"), status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        except:
            return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)

