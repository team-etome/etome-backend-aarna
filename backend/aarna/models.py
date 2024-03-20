from django.db import models
from app1.models import *
from flutter.models import *


class TimeTable(models.Model):
    exam_name          =   models.CharField(max_length=150)
    department         =   models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True )
    subject            =   models.ForeignKey(Subject, on_delete=models.CASCADE, null=True, blank=True )
    exam_date          =   models.DateField()
    exam_time          =   models.CharField(max_length = 30)
    

class Attendance(models.Model):

    sign_data     =    models.JSONField()  
    student       =    models.ForeignKey(Student,on_delete=models.CASCADE,null = True , blank = True)
    time_table    =    models.ForeignKey(TimeTable , on_delete = models.CASCADE, null = True , blank =True)


