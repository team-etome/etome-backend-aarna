from rest_framework import serializers
from app1.models import *



class QuestionPaperSerializer(serializers.ModelSerializer):
     class Meta:
        model   =  QuestionPaper
        fields = ['examName','department','subject','total_time','exam_date','vetTeacher1','term','semester']

