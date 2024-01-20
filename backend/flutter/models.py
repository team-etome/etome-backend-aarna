from django.db import models
from app1.models import *



class Questions(models.Model):
    questionpaper = models.ForeignKey(QuestionPaper , models.CASCADE , null = True , blank = True )
    questioncode  = models.CharField(max_length = 10 )
    
class QuestionImage(models.Model):
    question  = models.ForeignKey(Questions,models.CASCADE , null = True , blank = True)
    image     = models.ImageField(upload_to='question')



class Answer(models.Model):
    studentId     = models.CharField(max_length=50)
    questionCode  = models.CharField(max_length=50)
    date          = models.CharField(max_length=50)
    answerData    = models.JSONField()
    

class Evaluation(models.Model):
    studentId     = models.CharField(max_length=50)
    questionCode  = models.CharField(max_length=50)
    teacherId     = models.CharField(max_length=50)
    markData      = models.JSONField()
    totalMark     = models.CharField(max_length=50)
    date     = models.CharField(max_length=50)


