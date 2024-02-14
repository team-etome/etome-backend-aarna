from rest_framework import status
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
    def get(self, request):
        try:
            questionpapers = QuestionPaper.objects.all().order_by('exam_date')
            for questionpaper in questionpapers:
                try:
                    TimeTable.objects.create(
                        exam_name=questionpaper.exam_name,
                        department=questionpaper.department.department,
                        subject=questionpaper.subject.subject,
                        exam_date=questionpaper.exam_date,
                        exam_time=questionpaper.total_time,
                    )
                except Exception as e:
                    # print(f"Error creating timetable entry: {e}")
                    return JsonResponse(f"An error occurred: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return JsonResponse("Timetable entries created successfully", status=status.HTTP_200_OK)
        except Exception as e:
            # Handle broader exceptions or log them
            return JsonResponse(f"An error occurred: {e}", status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EvaluationAssign(APIView):

 
    def distribute_papers_to_teachers(self,teachers, answer_papers):
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
                answer_papers[student.roll_no] = answer_data

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
                return JsonResponse({'message': 'AssignEvaluation objects updated or created successfully'})

            print(AssignEvaluation,"lllllllllllllllllllllllllllllllllllllll")

            return JsonResponse("Evaluation assignments updated successfully.")

        except Department.DoesNotExist:
            return JsonResponse("Department not found", status=404)
        except Subject.DoesNotExist:
            return JsonResponse("Subject not found", status=404)

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
            try:
                # Handling answer image
                format, imgstr = answer_image_data.split(';base64,')
                answer_img = ContentFile(base64.b64decode(imgstr), name='answer.' + ext)
                AnswerImage.objects.create(question=question, image=answer_img)
            except Exception as e:
                question.delete()  # Rollback if answer image creation fails
                return JsonResponse({"success": False, "message": f"Error saving answer image: {e}"}, status=500)
            return JsonResponse({"success": True, "message": "Question and answer images successfully saved."}, status=200)

        except QuestionPaper.DoesNotExist:
                return JsonResponse({"success": False, "message": "QuestionPaper not found."}, status=404)

        except Exception as e:
                return JsonResponse({"success": False, "message": str(e)}, status=500)

class InvgilatorLogin(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            teacher = Teacher.objects.get(email=email)
        except Teacher.DoesNotExist:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)

        if teacher is not None and check_password(password, teacher.password):
            teacher_token = get_token(teacher, user_type='teacher') 

            seating_arrangement_details = []
            try:
                seating_arrangements = SeatingArrangement.objects.filter(teacher=teacher)
                
                for seating in seating_arrangements:
                    seating_arrangement_details.append({
                        'hall_name': seating.hall_name,
                        'department_students': seating.department_students, 
                    })

                department_ids = [json.loads(seating.department_ids) for seating in seating_arrangements if seating.department_ids]  
                department_ids = [item for sublist in department_ids for item in sublist]  

                question_papers = QuestionPaper.objects.filter(department__id__in=department_ids)

                question_paper_details = []
                for qpaper in question_papers:
                    questions = Questions.objects.filter(questionpaper=qpaper)
                    question_images = QuestionImage.objects.filter(question__in=questions)

                    images = [qimage.image.url for qimage in question_images]
                    question_paper_details.append({
                        'question_paper_id': qpaper.id,
                        'exam_name': qpaper.exam_name,
                        'department': qpaper.department.department, 
                        'images': images,
                    })

                response_data = {
                    'message': 'Login successful',
                    'token': teacher_token,
                    'question_papers': question_paper_details,
                    'seating_arrangements': seating_arrangement_details,  
                }

                return JsonResponse(response_data, status=200)

            except SeatingArrangement.DoesNotExist:
                return JsonResponse({'message': 'Login successful', 'token': teacher_token, 'error': 'No seating arrangement found for this teacher.'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        


        

        



            

        

        

        