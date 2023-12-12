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
    emailid                  =   models.EmailField()
    password                 =   models.CharField()
    address                  =   models.CharField(max_length=200)
    university               =   models.CharField(max_length=200)
    phn_number               =   models.CharField()





class Department(models.Model):
    department         =    models.CharField(max_length=50 , null=True)
    department_head    =    models.CharField(max_length=50, null=True)




class Subject(models.Model):
    Subject         = models.CharField(max_length=50,null=True)
    Subject_code    = models.IntegerField(null=True)
    programme       = models.CharField(max_length=50 , null=True)  




class Semester(models.Model):
    semester = models.CharField(max_length=12)



class Teacher(models.Model):
    department    = models.ForeignKey(Department , on_delete=models.CASCADE , null=True , blank=True)
    Subject       = models.ForeignKey(Subject ,on_delete=models.CASCADE , null=True ,blank=True )
    semester      = models.ForeignKey(Semester , on_delete=models.CASCADE , null=True , blank=True) 
    name          = models.CharField(max_length=50)
    email         = models.EmailField(unique=True,blank=True)
    empid         = models.CharField(max_length=20,blank=True)
    image         = models.ImageField(blank=True,null=True , upload_to='teacher')
    phoneNumber   = models.IntegerField(null=True)
    password      = models.CharField(max_length=10,blank=True)
    acoe          = models.BooleanField(default=False)
    hod           = models.BooleanField(default=False)




# class Hod(models.Model):
#     teacher     = models.ForeignKey(Teacher , on_delete=models.CASCADE , null=True ,blank=True)
#     department  = models.ForeignKey(Department , on_delete=models.CASCADE , null=True , blank=True)





class Student(models.Model):
    Semester      = models.ForeignKey(Semester , models.CASCADE ,null=True , blank=True)
    Subject       = models.ForeignKey(Subject,models.CASCADE,null=True , blank=True)
    studentName   = models.CharField(max_length=50)
    roll_no       = models.CharField(max_length=100)
    email         = models.EmailField(unique=True)
    number        = models.CharField(max_length=15)
    

    
    
    

    




