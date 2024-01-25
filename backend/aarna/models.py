from django.db import models
from app1.models import *
from flutter.models import *


class TimeTable(models.Model):
    exam_name          =   models.CharField(max_length=150)
    department         =   models.ForeignKey(Department, on_delete=models.CASCADE)
    Subject            =   models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_date          =   models.DateField()
    exam_time          =   models.CharField(max_length = 30)

