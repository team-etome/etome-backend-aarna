from rest_framework import serializers
from aarna.models import *



class TimeTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeTable
        fields = ['id','exam_name','department','subject','exam_date','exam_time']

class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model=Attendance
        fields=['sign_data','student','time_table']



class McqQuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model=McqQuestion
        fields=['question','subject','date','answer','id']