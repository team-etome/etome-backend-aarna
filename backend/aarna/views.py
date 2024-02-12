from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app1.models import *
from flutter.models import *
from .models import *
from app1.serializers import * 
from aarna.serializers import *
from flutter.serializers import * 
from rest_framework.exceptions import ValidationError
from app1.token import get_token
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.conf import settings
import json
import random
import string
import base64
from django.core.files.base import ContentFile



class Timetable(APIView):

    def get(self , request):
        try:
            questionpapers = QuestionPaper.objects.all().order_by('exam_date')
            for questionpaper in questionpapers:
                TimeTable.objects.create(
                    exam_name=questionpaper.exam_name,
                    department=questionpaper.department,
                    subject=questionpaper.subject,
                    exam_date=questionpaper.exam_date,
                    exam_time=questionpaper.total_time,
                )
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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
            return JsonResponse("Department not found", status=404)
        except Subject.DoesNotExist:
            return JsonResponse("Subject not found", status=404)
        except Exception as e:
            return JsonResponse(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class HallTicket(APIView):

    def get(self, request, *args, **kwargs):
        data = request.data
        roll_number = data.get('roll_no') 
        try:
            student = Student.objects.get(roll_no=roll_number)
            student_serializer = StudentSerializer(student)

            timetable = TimeTable.objects.filter(department_id=student.department_id).order_by('exam_date')
            timetable_serializer = TimeTableSerializer(timetable, many=True)  

         
            response_data = {
                'student'         : student_serializer.data,
                'department_name' : student.department.department,
                'image_url'       : student.image.url ,
                'timetable'       : timetable_serializer.data
            }

            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return JsonResponse({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return JsonResponse({"detail":str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class QuestionsView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            question_id = request.POST.get('question_id')
            question_image_data = request.POST.get('questionImage')
            answer_image_data = request.POST.get('answerImage')

            if not all([question_id, question_image_data, answer_image_data]):
                # If any of the required parameters are missing
                return JsonResponse({"success": False, "message": "Missing required parameters."}, status=400)

            question_paper = QuestionPaper.objects.get(pk=question_id)

            # Generate a random question code
            question_code = ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=5))

            # Create a new Questions object
            question = Questions.objects.create(
                questionpaper_id=question_id,
                questioncode=question_code
            )

            # Handling question image
            format, imgstr = question_image_data.split(';base64,')
            ext = format.split('/')[-1]
            question_img = ContentFile(base64.b64decode(imgstr), name='question.' + ext)
            QuestionImage.objects.create(question=question, image=question_img)

            # Handling answer image
            format, imgstr = answer_image_data.split(';base64,')
            answer_img = ContentFile(base64.b64decode(imgstr), name='answer.' + ext)
            AnswerImage.objects.create(question=question, image=answer_img)

            return JsonResponse({"success": True, "message": "Question and answer images successfully saved."}, status=200)

        except QuestionPaper.DoesNotExist:
                return JsonResponse({"success": False, "message": "QuestionPaper not found."}, status=404)

        except (ValueError, KeyError) as e:
                return JsonResponse({"success": False, "message": str(e)}, status=400)

        except AttributeError as e:
                return JsonResponse({"success": False, "message": "Invalid image data provided."}, status=400)

        except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)


        # try:
        #     question_paper = QuestionPaper.objects.get(pk=question_id)

        #     # Generate a random question code
        #     question_code = ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=5))


        #     # Create a new Questions object
        #     question = Questions.objects.create(
        #         questionpaper_id=question_id,  
        #         questioncode=question_code
        #     )

        #     format, imgstr = question_image_data.split(';base64,')
        #     ext = format.split('/')[-1]
        #     question_img = ContentFile(base64.b64decode(imgstr), name='question.' + ext)
        #     QuestionImage.objects.create(question=question, image=question_img)

        #     # Handling answer image
        #     format, imgstr = answer_image_data.split(';base64,')
        #     answer_img = ContentFile(base64.b64decode(imgstr), name='answer.' + ext)
        #     AnswerImage.objects.create(question=question, image=answer_img)

        #     return JsonResponse({"success": True, "message": "Question and answer images successfully saved."}, status=200)

        # except QuestionPaper.DoesNotExist:
        #     return JsonResponse({"success": False, "message": "QuestionPaper not found."}, status=404)

        # except Exception as e:
        #     return JsonResponse({"success": False, "message": str(e)}, status=500)


        

        



            

        

        

        