from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app1.models import *
from flutter.models import *
from .models import *
from app1.serializers import * 
from flutter.serializers import * 
from rest_framework.exceptions import ValidationError
from app1.token import get_token
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.conf import settings




class Timetable(APIView):

    def get(self , request):
        questionpapers = QuestionPaper.objects.all().order_by('exam_date')


        for questionpaper in questionpapers:
            TimeTable.objects.create(
                exam_name=questionpaper.exam_name,
                department=questionpaper.department,
                subject=questionpaper.subject,
                exam_date=questionpaper.exam_date,
                exam_time=questionpaper.total_time,
            )


class EvaluationView(APIView):
    def get(self, request, *args, **kwargs):


        # Get the number of teachers and total number of students from the request
        num_teachers = int(request.GET.get('teachers', 0))
        num_students = int(request.GET.get('students', 0))

        # Validate inputs
        if num_teachers <= 0 or num_students <= 0:
            return Response("Invalid input. Please provide a positive number of teachers and students.")

        # Generate example data for teachers and students
        teachers = [f"teach{i}" for i in range(1, num_teachers + 1)]
        students = [f"st{i}" for i in range(1, num_students + 1)]

        # Splitting logic based on the parity of teachers and students
        if num_teachers % 2 == 0 and num_students % 2 == 0:
            # Even teachers and even students: Assign students in a round-robin fashion
            assigned_students = {teacher: [] for teacher in teachers}
            for idx, student in enumerate(students):
                teacher = teachers[idx % num_teachers]
                assigned_students[teacher].append(student)

        elif num_teachers % 2 != 0 and num_students % 2 == 0:
            # Odd teachers and even students: Assign students sequentially to teachers
            assigned_students = {teachers[i]: students[i::num_teachers] for i in range(num_teachers)}

        elif num_teachers % 2 == 0 and num_students % 2 != 0:
            # Even teachers and odd students: Assign students in a round-robin fashion
            assigned_students = {teacher: [] for teacher in teachers}
            for idx, student in enumerate(students):
                teacher = teachers[idx % num_teachers]
                assigned_students[teacher].append(student)

        else:
            # Odd teachers and odd students: Assign students sequentially to teachers
            assigned_students = {teachers[i]: students[i::num_teachers] for i in range(num_teachers)}

        # Print the output to the terminal
        for teacher, students_list in assigned_students.items():
            print(f"{teacher} is assigned the following students: {students_list}")

        return Response("Output printed to the terminal.")  

class HallTicket(APIView):
    def get(self,request,id ,*args,**kwargs):
        
        st_id = id 
        student = Student.objects.get(id = st_id)
        department_id = student.department
        timetable = TimeTable.objects.filter(department_id = department_id).order_by('exam_date')

        studentdetails = []

        

        



            

        

        

        