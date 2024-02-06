from rest_framework import serializers
from aarna.models import *



class TimeTableSerializer(serializers.ModelSerializer):

    class Meta:
        model = TimeTable
        fields = ['exam_name','department','subject','exam_date','exam_time']

