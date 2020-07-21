from django.db import models
import uuid 

class School(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.UUIDField(max_length=200)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=100)
    address3 =  models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state =  models.CharField(max_length=50)
    zip = models.IntegerField(max_length=6)

    def __str__(self):
        return self.userid

class Admin(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.UUIDField(max_length=200)
    mobile = models.IntegerField(max_length=10)

class Student(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.UUIDField(max_length=200)
    schoolid = models.CharField(max_length=200)
    classid = models.CharField(max_length=200)
    dob = models.DateTimeField("mm-dd-yyyy")
    fathername = models.CharField(max_length=100)
    mothername = models.CharField(max_length=100)
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    address3 =  models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state =  models.CharField(max_length=50)
    zip = models.IntegerField(max_length=6)
    admissiondate = models.DateTimeField("mm-dd-yyyy")
    srno =  models.IntegerField(max_length=200)
    promotedclassid = models.CharField(max_length=100)

    def __str__(self):
        return self.userid

class FeeStructure(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    classid = models.CharField(max_length=200)
    feename = models.CharField(max_length=100)
    cycle = models.IntegerField(max_length=100)
    amount = models.IntegerField(max_length=100) 
    def __str__(self):
        return self.feename 

class Class(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    schoolid = models.CharField(max_length=200)
    classname = models.IntegerField(max_length=2)
    section = models.IntegerField(max_length=1)
    def __str__(self):
        return self.classname 

class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.CharField(max_length=100)
    classid = models.IntegerField(max_length=100)
    attendancedate = models.DateTimeField("mm-dd-yyyy")
    status = models.CharField(max_length=1)

    def __str__(self):
        return self.userid

class FeeDeposit(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.CharField(max_length=100)
    feestructureid = models.IntegerField(max_length=100)
    depositdate = models.DateTimeField("mm-dd-yyyy")
    depositamount = models.CharField(max_length=100)
    def __str__(self):
        return self.userid

class Homework(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    classid = models.CharField(max_length=100)
    homeworkdate = models.DateTimeField("mm-dd-yyyy")
    homework = models.CharField(max_length=100)
    def __str__(self):
        return self.classid

class TransferCertificate(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    userid = models.CharField(max_length=100)
    requestedby = models.CharField(max_length=100)
    approvedby = models.CharField(max_length=100)
    requestdate = models.DateTimeField("mm-dd-yyyy")
    approvedate = models.DateTimeField("mm-dd-yyyy")
    status = models.CharField(max_length=100)       

    def __str__(self):
        return self.requestedby