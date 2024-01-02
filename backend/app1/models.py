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
    department_code    =    models.CharField(null=True)
    department_head    =    models.CharField(max_length=50, null=True)




class Subject(models.Model):
    subject         = models.CharField(max_length=50,null=True)
    subject_code    = models.CharField(null=True)
    programme       = models.CharField(max_length=50 , null=True)  




class Semester(models.Model):
    semester        = models.CharField(max_length=12)



class Teacher(models.Model):
    department    =  models.ForeignKey(Department , on_delete=models.CASCADE , null=True , blank=True)
    Subject       =  models.ForeignKey(Subject ,on_delete=models.CASCADE , null=True ,blank=True )
    semester      =  models.ForeignKey(Semester , on_delete=models.CASCADE , null=True , blank=True) 
    name          =  models.CharField(max_length=50)
    email         =  models.EmailField(unique=True,blank=True)
    empid         =  models.CharField(max_length=20,blank=True)
    image         =  models.ImageField(blank=True,null=True , upload_to='teacher')
    phoneNumber   =  models.IntegerField(null=True)
    password      =  models.CharField(max_length=10,blank=True)
    acoe          =  models.BooleanField(default=False)
    hod           =  models.BooleanField(default=False)
    vetTeacher    =  models.BooleanField(default = False)





class Student(models.Model):
    Semester      =  models.ForeignKey(Semester , models.CASCADE ,null=True , blank=True)
    Subject       =  models.ForeignKey(Subject,models.CASCADE,null=True , blank=True)
    department    =  models.ForeignKey(Department , models.CASCADE , null=True , blank=True)
    studentName   =  models.CharField(max_length=50)
    roll_no       =  models.CharField(max_length=100,unique=True)
    email         =  models.EmailField(unique=True)
    number        =  models.CharField(max_length=15)
    password      =  models.CharField(max_length=10 , blank=True , null=True),
    dob           =  models.DateField(null = True)
    

# class QuestionPaper(models.Model):
#     examName        =  models.CharField(max_length = 15)
#     department      =  models.ForeignKey(Department , models.CASCADE , null = True , blank = True)
#     subject         =  models.ForeignKey(Subject , models.CASCADE , null = True , blank = True) 
#     total_time      =  models.TimeField()
#     exam_date       =  models.DateField()
#     vetTeacher1     =  models.ForeignKey(Teacher , models.CASCADE , blank = True , null = True)
#     send_Blueprint  =  models.BooleanField(default = False)


# class Blueprint(models.Model):
#     question_paper = models.OneToOneField(QuestionPaper, on_delete=models.CASCADE, related_name='blueprint')
#     module_1_section_a = models.PositiveIntegerField(default=0)
#     module_2_section_a = models.PositiveIntegerField(default=0)
#     module_3_section_a = models.PositiveIntegerField(default=0)
#     module_4_section_a = models.PositiveIntegerField(default=0)
#     module_5_section_a = models.PositiveIntegerField(default=0)
    
#     module_1_section_b = models.PositiveIntegerField(default=0)
#     module_2_section_b = models.PositiveIntegerField(default=0)
#     module_3_section_b = models.PositiveIntegerField(default=0)
#     module_4_section_b = models.PositiveIntegerField(default=0)
#     module_5_section_b = models.PositiveIntegerField(default=0)
    
#     module_1_section_c = models.PositiveIntegerField(default=0)
#     module_2_section_c = models.PositiveIntegerField(default=0)
#     module_3_section_c = models.PositiveIntegerField(default=0)
#     module_4_section_c = models.PositiveIntegerField(default=0)
#     module_5_section_c = models.PositiveIntegerField(default=0)
    
#     total_questions_section_a = models.PositiveIntegerField(default=0)
#     total_questions_section_b = models.PositiveIntegerField(default=0)
#     total_questions_section_c = models.PositiveIntegerField(default=0)
    
#     compulsory_section_a = models.PositiveIntegerField(default=0)
#     compulsory_section_b = models.PositiveIntegerField(default=0)
#     compulsory_section_c = models.PositiveIntegerField(default=0)
    
   
#     total_weightage_section_a = models.CharField(max_length=100)
#     total_weightage_section_b = models.CharField(max_length=100)
#     total_weightage_section_c = models.CharField(max_length=100)
    
  
#     approved = models.BooleanField(default=False)



    

    




