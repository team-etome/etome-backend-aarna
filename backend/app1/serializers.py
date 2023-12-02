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
        fields = ['department']




class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subject
        fields = ['Subject']



class Semester(serializers.ModelSerializer):

    class Meta:
        model = Semester
        fields = ['semester']


class Teacher(serializers.ModelSerializer):

    class Meta:
        model = Semester
        fields = ['department','Subject','semester','teacherName']



class Hod(serializers.ModelSerializer):

    class Meta:
        model = Hod
        fields = ['teacher',"department"]



class Student(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ['studentName',"roll_no"]