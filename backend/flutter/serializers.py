from rest_framework import serializers
from flutter.models import *
from app1.models import *
from django.contrib.auth.hashers import make_password



# class DataSerializer(serializers.ModelSerializer):


# class Meta:
#     model = Byte
#     fields = ['image_name','data']


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = [
            'studentName',
            'roll_no',
            'semester',
            'department',
            'number',
            'email',
            'gender',
            'dob',
            'password',
            'parent_name',
            'parent_email',
            'parent_contact_number',
            'parent_relation',
            'image',
            'address'
        ]

    # def create(self, validated_data):
    #     password = validated_data.pop('password', None)
    #     instance = self.Meta.model(**validated_data)
    #     if password is not None:
    #         instance.password = make_password(password)
    #     instance.save()
    #     return instance
        
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['student', 'question_code', 'date', 'answer_data']
        
class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = ['student', 'question_code', 'teacher','mark_data','total_mark','date']