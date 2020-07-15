from django.db import models
import uuid 

# Create your models here.

class Login(models.Model):
    Role = (('Admin','Admin'), 
            ('School', 'School'), 
            ('Accountant', 'Accountant'), 
            ('Teacher', 'Teacher'),
            ('Reception','Reception'), 
            ('Student','Student'))
    id = models.UUIDField(primary_key=True, default= uuid.uuid4, editable=False, max_length=200)
    name = models.CharField(max_length=80)
    image = models.CharField(max_length=1000)
    email  = models.EmailField(max_length=200, unique=True)
    password =  models.CharField(max_length=200)
    role = models.CharField(max_length=200, choices=Role, default='Student')
    active =  models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ErrorMessage(models.Model):
    code = models.CharField(max_length=80)
    message =  models.CharField(max_length=80)
    
    def __str__(self):
        return self.code