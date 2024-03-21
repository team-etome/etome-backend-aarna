from rest_framework import status
from rest_framework.views import APIView
from app1.models import *
from flutter.models import *
from .models import *
from app1.serializers import * 
from aarna.serializers import *
from flutter.serializers import * 
from app1.token import get_token
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
import json
import random
import string
import base64
from django.core.files.base import ContentFile
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from datetime import datetime
from django.db import transaction



class EvaluationAssign(APIView):
    def distribute_papers_to_teachers(self, teachers, students):
        num_teachers = len(teachers)
        assigned_papers = {teacher.id: [] for teacher in teachers}
        all_students = list(students)
        idx = 0 
        while all_students:
            teacher = teachers[idx % num_teachers]
            student = all_students.pop(0)  
            assigned_papers[teacher.id].append(student)
            idx += 1
        return assigned_papers
    def post(self, request, *args, **kwargs):
        data = request.data
        department_name = data.get('department')
        semester = data.get('semester')
        subject_id = data.get('subject')
        endDate = data.get('endDate')
        term = data.get('term')
        try:
            department = Department.objects.get(department=department_name)
            subject = Subject.objects.get(id=subject_id)
            print(subject)
            students = Student.objects.filter(department=department).values_list('roll_no', flat=True)
            teachers = Teacher.objects.filter(id__in=data.get('teacher', []))
            if not  students.exists():
                return JsonResponse({"error": "No students found"},status=403)
            distributed_papers = self.distribute_papers_to_teachers(teachers, students)
            for teacher, student_roll_numbers in distributed_papers.items():
                AssignEvaluation.objects.update_or_create(
                    department=department,
                    semester=semester,
                    subject=subject,
                    teacher_id=teacher,
                    defaults={
                        'students': json.dumps(student_roll_numbers),
                        'endDate': endDate,
                        'term': term,
                    }
                )
            return JsonResponse({'message': 'AssignEvaluation objects updated or created successfully'})
        except Department.DoesNotExist:
            return JsonResponse("Department not found", status=404)
        except Subject.DoesNotExist:
            return JsonResponse("Subject not found", status=404)
        

    def get(self, request, *args, **kwargs):
        department_id = request.query_params.get('department_id')
        semester = request.query_params.get('semester')
        subject_id = request.query_params.get('subject_id')
        teacher_id = request.query_params.get('teacher_id')
        filters = {}
        if department_id:
            filters['department_id'] = department_id
        if semester:
            filters['semester'] = semester
        if subject_id:
            filters['subject_id'] = subject_id
        if teacher_id:
            filters['teacher_id'] = teacher_id
        try:
            evaluations = AssignEvaluation.objects.filter(**filters)
            evaluation_data = []
            for evaluation in evaluations:
                evaluation_data.append({
                    'department': evaluation.department.department,
                    'semester': evaluation.semester,
                    'subject': evaluation.subject.subject,
                    'teacher': evaluation.teacher.name if evaluation.teacher else None,
                    'endDate': evaluation.endDate,
                    'term': evaluation.term,
                    'students': evaluation.students
                })
            return Response(evaluation_data, status=status.HTTP_200_OK)
        except AssignEvaluation.DoesNotExist:
            return Response({"error": "No evaluations found"}, status=status.HTTP_404_NOT_FOUND)

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
                'timetable'       : timetable_serializer.data,
                'student_id'      : student.id,
                
 

            }

            print(response_data,"rrrrrrrrrrrrrrrrrrrrrrr")

            return JsonResponse(response_data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return JsonResponse({"detail": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        
        except TimeTable.DoesNotExist:
            return JsonResponse({"detail": "timetable not found"}, status=403)

class QuestionsView(APIView):

    def post(self, request, *args, **kwargs):

        try:
            question_id = request.POST.get('question_id')
            question_image_data = request.POST.get('questionImage')
            answer_image_data = request.POST.get('answerImage')

            if not all([question_id, question_image_data, answer_image_data]):
                return JsonResponse({"success": False, "message": "Missing required parameters."}, status=400)

            question_paper = QuestionPaper.objects.get(pk=question_id)

            question_code = ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=5))

            question = Questions.objects.create(
                questionpaper_id=question_id,
                questioncode=question_code
            )

            format, imgstr = question_image_data.split(';base64,')
            ext = format.split('/')[-1]
            question_img = ContentFile(base64.b64decode(imgstr), name='question.' + ext)
            QuestionImage.objects.create(question=question, image=question_img)
            try:
                format, imgstr = answer_image_data.split(';base64,')
                answer_img = ContentFile(base64.b64decode(imgstr), name='answer.' + ext)
                AnswerImage.objects.create(question=question, image=answer_img)
            except Exception as e:
                question.delete()
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
        current_datetime = datetime.now() 
        try:
            teacher = Teacher.objects.get(email=email)
            teacher_id=teacher.id
            seating=SeatingArrangement.objects.get(teacher_id=teacher_id)
            seating_id=seating.id
            if not check_password(password, teacher.password):
             return JsonResponse({'error': 'Invalid email or password'}, status=401)
        except Teacher.DoesNotExist:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)
        try:
            teacher_token = get_token(teacher, user_type='teacher')
        except Exception as e:  
            return JsonResponse({'error': 'Failed to generate token'}, status=500)
        seating_arrangement_details = []
        seating_arrangements = SeatingArrangement.objects.filter(teacher=teacher)
        for seating in seating_arrangements:
            seating_arrangement_details.append({
                'hall_name': seating.hall_name,
                'department_students': seating.department_students,
                'pattern':seating.pattern,
            })
        question_paper_details = []
        department_ids = [json.loads(seating.department_ids) for seating in seating_arrangements if seating.department_ids]
        department_ids = [item for sublist in department_ids for item in sublist]
        question_papers = QuestionPaper.objects.filter(department__id__in=department_ids,exam_date=current_datetime.date())
        for qpaper in question_papers:
            questions = Questions.objects.filter(questionpaper=qpaper)
            question_images = QuestionImage.objects.filter(question__in=questions)
            images = [qimage.image.url for qimage in question_images]
            start_time = qpaper.start_time
            end_time   = qpaper.end_time
            
            start_time_str = start_time.strftime('%H:%M')
            end_time_str = end_time.strftime('%H:%M')

            question_paper_details.append({
                'question_paper_id': qpaper.id,
                'exam_name': qpaper.exam_name,
                'department': qpaper.department.department,
                'start_time' : start_time_str,
                'end_time' : end_time_str ,
                'images': images,
                'seating_id':seating_id,

            })
        if not seating_arrangement_details :
            return JsonResponse({'error': 'Login cannot proceed due to missing seating arrangements '}, status=403)
        elif not question_paper_details:
            return JsonResponse({'error': 'Login cannot proceed due to missing question papers.'}, status=404)
        else:
            response_data = {
                'message': 'Login successful',
                'token': teacher_token,
                'question_papers': question_paper_details,
                'seating_arrangements': seating_arrangement_details,
            }
            return JsonResponse(response_data, status=200)
        


class Attendanceview(APIView):
    parser_classes = [JSONParser]

    def post(self, request, *args, **kwargs):
        
        attendance_records = request.data.get('sign_data', [])
        if not isinstance(attendance_records , list):
            return JsonResponse({'error': 'Invalid data format, expected a list.'}, status=400)

        for item in attendance_records :
            if not isinstance(item, dict):
                return JsonResponse({'error': 'Invalid item format, expected a dictionary.'}, status=400)
            
            try:
                student_id = item.get('studentId')
                student_signature = item.get('studentSignature')  
                time_table_id = item.get('timeTableId')

                student_instance = Student.objects.get(roll_no=student_id)
                time_table_instance = TimeTable.objects.get(id=time_table_id)

                print(student_signature)

                Attendance.objects.create(
                    sign_data=student_signature,
                    student=student_instance,
                    time_table=time_table_instance
                )

            except Student.DoesNotExist:
                return JsonResponse({'error': f'Student with ID {student_id} does not exist.'}, status=400)
            except TimeTable.DoesNotExist:
                return JsonResponse({'error': f'TimeTable with ID {time_table_id} does not exist.'}, status=400)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)

        return JsonResponse({'message': 'Attendance data stored successfully.'}, status=201)



class CreateMcqQuestion(APIView):
    def post(self, request, *args, **kwargs):
        question_data = {
            'question': request.data.get('question'),
            'options': request.data.get('options')  
        }
        subject = request.data.get('subject')
        date = request.data.get('date')
        correctAnswer = request.data.get('correctAnswer') 

     
        
        mcq_question = McqQuestion.objects.create(
            
            question=question_data,
            subject=subject,
            date=date,
            answer=correctAnswer
        )

        return Response({'message': 'MCQ question created successfully.'}, status=status.HTTP_201_CREATED)
        

class McqLogin(APIView):

    def post(self, request, *args, **kwargs):
        roll_no = request.data.get('roll_no')
        password = request.data.get('password')

        try:
            user = Student.objects.get(roll_no=roll_no)
            if user and check_password(password, user.password):
                mcq_questions = McqQuestion.objects.order_by('?')
                serialized_questions = McqQuestionSerializer(mcq_questions, many=True).data
                questions_data = [{'id': question['id'], 'question': question['question']} for question in serialized_questions]
                return JsonResponse({'questions': questions_data})

        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    

    
class McqEvaluation(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        roll_no = data.get('roll_no')
        questions = data.get('questions', [])
        
        try:
            student = Student.objects.get(roll_no=roll_no)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
        
        score = 0
        
        with transaction.atomic():
            for item in questions:
                question_data = item.get('question', {})
                question_id = question_data.get('id')
                selected_option = question_data.get('selectedOption')
                try:
                    question = McqQuestion.objects.get(id=question_id)
                    if question.answer == selected_option:
                        score += 4
                    else:
                        score -= 1
                except McqQuestion.DoesNotExist:
                   
                    pass
            McqResult.objects.create(student=student, marks=score)
            return JsonResponse({'message': 'Results saved successfully', 'score': score})
        

    def get(self, request):

        results = McqResult.objects.all()
        evaluation_result = []
        for result in results:
            
            evaluation_result.append(
                {
                    'student_name': result.student.student_name,
                    'mark'        : result.marks

                }
            )
        return JsonResponse(evaluation_result, safe=False, status=status.HTTP_200_OK)



       
