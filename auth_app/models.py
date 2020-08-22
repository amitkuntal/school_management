from django.db import models
import uuid 
import datetime

def upload_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(uuid.uuid4().hex, ext)
    return '/'.join(['profile',filename])

class School(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.UUIDField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=100)
    address3 =  models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state =  models.CharField(max_length=50)
    zip = models.CharField(max_length=7)

    def __str__(self):
        return self.userid

class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.UUIDField(max_length=200)
    mobile = models.CharField(max_length=10)

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.UUIDField(max_length=200)
    schoolid = models.CharField(max_length=200)
    classid = models.CharField(max_length=200, default='')
    dob = models.DateField()
    fathername = models.CharField(max_length=100)
    mothername = models.CharField(max_length=100)
    mobileno1 = models.CharField(max_length=10)
    mobileno2 = models.CharField(max_length=10)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 =  models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state =  models.CharField(max_length=50)
    zip = models.IntegerField()
    admissiondate = models.DateField()
    srno =  models.IntegerField()
    promotedclassid = models.CharField(max_length=100)

    def __str__(self):
        return self.userid

class FeeStructure(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=100)
    classid = models.CharField(max_length=100)
    schoolid = models.CharField(max_length=100)
    feename = models.CharField(max_length=100)
    cycle = models.IntegerField()
    amount = models.IntegerField() 
    def __str__(self):
        return self.feename 

class Class(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    schoolid = models.CharField(max_length=100)
    classname = models.CharField(max_length=3)
    section = models.CharField(max_length=2,default="",blank=True)
    def __str__(self):
        return self.classname 

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.CharField(max_length=100)
    schoolid = models.CharField(max_length=100)
    classid = models.CharField(max_length=100)
    attendancedate = models.DateField(default=datetime.date.today())
    status = models.CharField(max_length=1, default='A')

    def __str__(self):
        return self.userid

class FeeDeposit(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.CharField(max_length=100)
    schoolid = models.CharField(max_length=100)
    classid = models.CharField(max_length=100)
    feestructureid = models.CharField(max_length=100)
    depositdate = models.DateField()
    depositamount = models.CharField(max_length=100)
    def __str__(self):
        return self.userid

class Homework(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    classid = models.CharField(max_length=100)
    teacherid = models.CharField(max_length=100)
    homeworkdate = models.DateField(default=datetime.date.today())
    image = models.BinaryField(blank=True)
    homework = models.CharField(max_length=800, blank = True, null = True)
    def __str__(self):
        return self.classid

class TransferCertificate(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.CharField(max_length=100)
    schoolid = models.CharField(max_length=200)
    requestedby = models.CharField(max_length=100)
    approvedby = models.CharField(max_length=100)
    requestdate = models.DateField()
    approvedate = models.DateField()
    status = models.CharField(max_length=100)       

    def __str__(self):
        return self.requestedby



class Login(models.Model):
    Role = (('Admin','Admin'), 
            ('School', 'School'), 
            ('Accountant', 'Accountant'), 
            ('Teacher', 'Teacher'),
            ('Reception','Reception'), 
            ('Student','Student'))
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    name = models.CharField(max_length=80)
    image = models.BinaryField(blank=False)
    email  = models.CharField(max_length=200, unique=True)
    password =  models.CharField(max_length=200)
    role = models.CharField(max_length=200, choices=Role, default='Student')
    active =  models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=100)
    userid = models.UUIDField(max_length=100)
    schoolid = models.CharField(max_length=100)
    mobile = models.CharField(max_length=10)
    classid = models.CharField(max_length=100)
    dob = models.DateField()
    fathername = models.CharField(max_length=100)
    mothername = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 =  models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state =  models.CharField(max_length=50)
    zip = models.CharField(max_length=7)
    dateOfJoining = models.DateField()
    salary = models.IntegerField()

    def __str__(self):
        return self.userid

class Subject(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=100)
    classid = models.CharField(max_length=100)
    subjectname = models.CharField(max_length=100)

    def __str__(self):
        return self.classid

class EducationPortal(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=100)
    subjectid = models.CharField(max_length=100)
    chaptername = models.CharField(max_length=100)
    videolink = models.CharField(max_length=500)

    def __str__(self):
        return self.subjectid

class EmployeeAttendance(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.CharField(max_length=100)
    attendancedate = models.DateField(default=datetime.date.today())
    status = models.CharField(max_length=1,default='A')

    def __str__(self):
        return self.userid

class TimeTable(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    schoolid = models.CharField(max_length=100)
    classid = models.CharField(max_length=100)
    subjectid = models.CharField(max_length=100)
    period = models.CharField(max_length=1)
    teacherid = models.CharField(max_length=100)
    day = models.CharField(max_length=12)
    
    def __str__(self):
        return self.schoolid




class ErrorMessage():
    code = models.CharField(max_length=80)
    message =  models.CharField(max_length=80)

class LoginPayload():
    email = models.EmailField(max_length=100,blank=False)
    password = models.CharField(max_length=100, blank=False)

class LoginResponse():
    accessToken  = models.CharField(max_length=1000)
    refreshToken = models.CharField(max_length=1000)
