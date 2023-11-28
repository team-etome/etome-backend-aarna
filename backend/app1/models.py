from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager



class God(AbstractUser):
    username    =  models.CharField(unique=True , null=True, blank=True)
    email       = models.EmailField(unique=True )






    
    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=[]

    def __str__(self):
        return self.email
    




class Admin(models.Model):

    instituteName            =   models.CharField(max_length=200)
    emailid                  =   models.EmailField(unique=True )
    principal                =   models.CharField(max_length=50)
    password                 =   models.CharField(unique=True)
    students_no              =   models.IntegerField()
    university               =   models.CharField(max_length=200)
    teacher_no               =   models.IntegerField()
    phn_number               =   models.IntegerField()





class Department(models.Model):
    admin              =    models.ForeignKey(Admin , on_delete=models.CASCADE,null=True , blank= True)
    department_name    =    models.CharField()
    




