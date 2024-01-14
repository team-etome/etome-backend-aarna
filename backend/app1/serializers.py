from rest_framework import serializers
from app1.models import *
from django.contrib.auth.hashers import make_password



class GodSerializer(serializers.ModelSerializer):

    class Meta:
        model = God
        fields = ['email','password']


class AdminSerializer(serializers.ModelSerializer):

    class Meta:
        model = Admin
        fields = ['instituteName','emailid','password','address','university','phn_number']


    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.password = make_password(password)
        instance.save()
        return instance




class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ['department','department_code','department_head']




class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['subject','subject_code','programme']



class SemesterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Semester
        fields = ['semester']


class TeacherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Teacher
        fields = ['departments', 'subjects', 'semester', 'name', 'email', 'image', 'phoneNumber', 'password']

    def create(self, validated_data):
        departments_data = validated_data.pop('departments', [])
        subjects_data = validated_data.pop('subjects', [])
        password = validated_data.pop('password', None)
        teacher = Teacher(**validated_data)

        if password is not None:
            teacher.password = make_password(password)
        teacher.save()

        for department in departments_data:
            teacher.departments.add(department)
        for subject in subjects_data:
            teacher.subjects.add(subject)

        return teacher



class BlueprintSerializer(serializers.ModelSerializer):

    class Meta:
        model   =  Blueprint
        fields = [
            'id',
            'question_paper',
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



