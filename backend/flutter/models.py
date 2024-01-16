from django.db import models



class Byte(models.Model):
    image_name   = models.CharField(max_length=50)
    data         = models.BinaryField()
    datas         = models.JSONField(null=True,blank=True)



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


