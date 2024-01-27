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
import json




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

class EvaluationAssign(APIView):

 
    def distribute_papers_to_teachers(teachers, answer_papers):
        num_teachers = len(teachers)
        assigned_papers = {teacher.id: [] for teacher in teachers}

        all_papers = [(student_roll, papers) for student_roll, papers in answer_papers.items()]
        idx = 0  # Index to iterate over papers

        while all_papers:
            teacher = teachers[idx % num_teachers]
            student_roll, papers = all_papers.pop(0)  # Get the first set of papers
            assigned_papers[teacher.id].append({student_roll: papers})
            idx += 1

        return assigned_papers

    def post(self, request, *args, **kwargs):
        data = request.data
        department_name = data.get('department')
        semester = data.get('semester')
        subject_id = data.get('subject')

        try:
            department = Department.objects.get(department=department_name)
            subject = Subject.objects.get(id=subject_id)
            students = Student.objects.filter(department=department)

            answer_papers = {}
            for student in students:
                questions = Questions.objects.filter(questionpaper__subject=subject)
                answers = Answer.objects.filter(student=student, question__in=questions)
                answer_data = [answer.answer_data for answer in answers]
                answer_papers[student.roll_number] = answer_data

            teachers = Teacher.objects.filter(id__in=data.get('teacher', []))

           
            distributed_papers = self.distribute_papers_to_teachers(teachers, answer_papers)

           
            for teacher_id, papers in distributed_papers.items():
                AssignEvaluation.objects.update_or_create(
                    department=department,
                    semester=semester,
                    subject=subject,
                    teacher_id=teacher_id,
                    defaults={'students': json.dumps(papers)}
                )

            return Response("Evaluation assignments updated successfully.")

        except Department.DoesNotExist:
            return Response("Department not found", status=404)
        except Subject.DoesNotExist:
            return Response("Subject not found", status=404)
    


class HallTicket(APIView):
    def get(self,request,id ,*args,**kwargs):
        
        student = Student.objects.get(id = id)
        department_id = student.department
        timetable = TimeTable.objects.filter(department_id = department_id).order_by('exam_date')

        studentdetails = []

        

        



            

        

        

        