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
        # except:
        #     return Response(dict(code="400", message="Something went"), status= status.HTTP_401_UNAUTHORIZED)

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
            return Response(dict(code="400", message="Something went wrong Token"), status= status.HTTP_401_UNAUTHORIZED)

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
                                image = request.data['image'],
                                password = pwd_context.encrypt(request.data['password'])))
                if(loginSerializer.is_valid()):
                    login  = Login(
                                name = request.data['name'],
                                email =  request.data['email'],
                                role = request.data['role'],
                                image = request.data['image'],
                                password = pwd_context.encrypt(request.data['password']))
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
        # except:
        #     return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)

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
                for user in data:
                    user['image'] = readFiles(user['image'])
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
        # except:
        #     return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



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
        # except:
        #     return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



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
            if(role in ['School', 'Reception','Teacher', 'Accountant']):
                video = EducationPortalSerializer(EducationPortal.objects.filter(subjectid__exact = request.data['subjectid']), many=True)
                return Response(video.data, status = status.HTTP_200_OK)
            return Response(dict(code="400", message="Unauthrized Access"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.ExpiredSignatureError:
            return Response(dict(code="400", message="Expired Signature"), status= status.HTTP_401_UNAUTHORIZED)
        except jwt.exceptions.DecodeError:
                return Response(dict(code="400", message="Invalid Token"), status= status.HTTP_401_UNAUTHORIZED)
        # except:
        #     return Response(dict(code="400", message="Something went wrong"), status= status.HTTP_401_UNAUTHORIZED)



    def delete(self, request):
        return Response(status=status.HTTP_404_NOT_FOUND)





