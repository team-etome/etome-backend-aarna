from django.db import models
from app1.models import *



class Questions(models.Model):
    questionpaper = models.ForeignKey(QuestionPaper ,on_delete=models.CASCADE , null = True , blank = True )
    questioncode  = models.CharField(max_length = 10 )



    
class QuestionImage(models.Model):
    question  = models.ForeignKey(Questions,on_delete=models.CASCADE , null = True , blank = True)
    image     = models.ImageField(blank=True,null=True ,upload_to='question')

class AnswerImage(models.Model):
    question  = models.ForeignKey(Questions,on_delete=models.CASCADE , null = True , blank = True)
    image     = models.ImageField(blank=True,null=True ,upload_to='answers')


class Answer(models.Model):
    student         =  models.ForeignKey(Student,on_delete=models.CASCADE,null = True , blank = True)
    question        =  models.ForeignKey(Questions ,on_delete=models.CASCADE , null = True , blank = True)
    date            =  models.CharField(max_length=50)
    answer_data     =  models.JSONField()
     # question_code   =  models.CharField(max_length=50)



class AssignEvaluation(models.Model):
    department     =  models.ForeignKey(Department , on_delete=models.CASCADE)
    semester       =  models.CharField(max_length = 20)
    subject        =  models.ForeignKey(Subject , on_delete=models.CASCADE)
    teacher        =  models.ForeignKey(Teacher , on_delete=models.CASCADE, null = True, blank= True)
    endDate        =  models.DateField()
    term           =  models.CharField(max_length =20 ,  null = True, blank= True)
    students       =  models.JSONField

    

class Evaluation(models.Model):

    answer         = models.ForeignKey(Answer ,on_delete=models.CASCADE,null = True , blank = True )
    mark_data      = models.JSONField()
    total_mark     = models.CharField(max_length=50)
    teacher        = models.ForeignKey(Teacher , on_delete=models.CASCADE, null = True, blank= True)
    date           = models.CharField(max_length=50)
    # student        = models.ForeignKey(Student ,on_delete=models.CASCADE, null = True, blank= True)
    # question_code  = models.CharField(max_length=50)


class SeatingArrangement(models.Model):

    PATTERN_CHOICES = [
        ('vertical_arrangement', 'vertical_arrangement'),
        ('horizondal_arranegement', 'horizondal_arranegement')
    ]

    pattern              =  models.CharField(max_length=50, choices=PATTERN_CHOICES)
    hall_name            =  models.CharField(max_length=100)
    teacher              =  models.ForeignKey(Teacher , on_delete = models.CASCADE ,null = True , blank = True)
    exam_name            =  models.CharField(max_length=100)
    exam_date            =  models.DateField()
    exam_time            =  models.CharField()
    seating_layout       =  models.CharField(max_length = 50, null = True , blank = True)
    department_students  =  models.JSONField(null=True, blank=True)
