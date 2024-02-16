from rest_framework import serializers
from app1.models import *
from flutter.models import *



class QuestionPaperSerializer(serializers.ModelSerializer):
     class Meta:
        model   =  QuestionPaper
        fields = ['id','exam_name','department','subject','start_time','exam_date','teacher','term','semester','end_time']


class BlueprintSerializer(serializers.ModelSerializer):

    class Meta:
        model   =  Blueprint
        fields = [
            'id',
            'question_paper',
            'vet_teacher',
            'module_1_section_a',
            'module_2_section_a',
            'module_3_section_a',
            'module_4_section_a',
            'module_5_section_a',

            'module_1_section_b',
            'module_2_section_b',
            'module_3_section_b',
            'module_4_section_b',
            'module_5_section_b',

            'module_1_section_c',
            'module_2_section_c',
            'module_3_section_c',
            'module_4_section_c',
            'module_5_section_c',

            'total_questions_section_a',
            'total_questions_section_b',
            'total_questions_section_c',

            'compulsory_section_a',
            'compulsory_section_b',
            'compulsory_section_c',
            
            'total_weightage_section_a',
            'total_weightage_section_b',
            'total_weightage_section_c',
        ]  



class SeatingArrangementSerializer(serializers.ModelSerializer):
     class Meta:
        model   = SeatingArrangement
        fields = ['id','pattern','hall_name','teacher','exam_name','exam_date','exam_time','department_students','seating_layout']
