from django.shortcuts import render
from rest_framework.views import APIView
from app1.models import *
from aarna.models import *
from app1.serializers import *
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from flutter.models import *
from .serializers import *
from rest_framework import status
from datetime import datetime
import json
import pandas as pd







class AddStudent(APIView):
   
    def post(self, request):
        mobile_number = request.data.get('number')
        roll_no = request.data.get('roll_no')
        email=request.data.get('email')
    
        if Student.objects.filter(number=mobile_number).exists():
            return JsonResponse({'message': 'A student with the same mobile number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if Student.objects.filter(roll_no=roll_no).exists():
            return JsonResponse({'message': 'A student with the same register number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        if Student.objects.filter(email=email).exists():
            return JsonResponse({'message':'a student with same email already exists'},status=status.HTTP_400_BAD_REQUEST)
        print(request.data)
        student_serializer = StudentSerializer(data=request.data)
        if student_serializer.is_valid():
            student_serializer.save()
            return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            print(student_serializer.errors)
            return JsonResponse(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    





class UploadExcelStudent(APIView):
    def post(self, request, *args, **kwargs):
        excel_file = request.FILES.get('file')

        if not excel_file:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)
        
        try:
        
            df = pd.read_excel(excel_file, engine='openpyxl')
            for _, row in df.iterrows():
                department_name = row.get('Department')
               
                department, _ = Department.objects.get_or_create(department=department_name)
                
          
                Student.objects.update_or_create(
                    roll_no=row.get('Roll Number'),
                    defaults={
                        'studentName': row['Student Name'],
                        'semester': row.get('Semester', None),
                        'department': department,
                        'number': row.get('Contact Number', None),
                        'email': row['Email'],
                        'gender': row.get('Gender', None),
                        'dob': pd.to_datetime(row['DOB (YYYY-MM-DD)']).date() if row.get('DOB (YYYY-MM-DD)', None) else None,
                        'password': row.get('Password', None),
                        
                    }
                )
            
            return JsonResponse({'message': 'Excel file processed successfully.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)



   
class StudentExaminationLogin(APIView):
    def post(self, request, *args, **kwargs):
        roll_no = request.data.get('roll_no')
        password = request.data.get('password')
        
       
        try:
            user = Student.objects.get(roll_no=roll_no)
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=409)
        current_date = datetime.now().date()

        current_time = datetime.now().time()
        department=user.department_id
        student_id=user.id
        questions=QuestionPaper.objects.filter(department_id=department,exam_date=current_date)
        for question in questions:
         if current_time >= question.start_time and current_time <= question.end_time:                
            if Answer.objects.filter(student_id=student_id,question_id=question.id).exists():
                    return JsonResponse({'error': 'Student already written the exam'}, status=404)
        


        if user is not None and check_password(password, user.password):
            current_datetime = datetime.now()
            department_id = user.department_id

            try:
                # Get all question papers for the department and current date
                questionpapers = QuestionPaper.objects.filter(department_id=department_id, exam_date=current_datetime.date())

                # Filter question papers based on current time
                questionpaper = None
                for qp in questionpapers:
                    if qp.start_time <= current_datetime.time() <= qp.end_time:
                        questionpaper = qp
                        break

                if questionpaper is None:
                    return JsonResponse({'error': 'No exam scheduled for now or for this department'}, status=405)

                questionpaper_id = questionpaper.id
                main_question = Questions.objects.filter(questionpaper=questionpaper).first()
                blueprint = Blueprint.objects.get(question_paper=questionpaper_id)
                total_questions = int(blueprint.total_questions)

                exam_end_datetime = datetime.combine(current_datetime.date(), questionpaper.end_time)
                remaining_time = round((exam_end_datetime - current_datetime).total_seconds() / 60)
                question_paper_details = {
                    'student_id': user.id,
                    'exam_name': questionpaper.exam_name,
                    'total_time': remaining_time,
                    'semester': questionpaper.semester,
                    'department': questionpaper.department.department,
                    'subject': questionpaper.subject.subject,
                    'subject_code': questionpaper.subject.subject_code,
                    'teacher': questionpaper.teacher.name,
                    'question_id': main_question.id,
                    'question_code': main_question.questioncode,
                    'total_question': total_questions
                }

                question_image = QuestionImage.objects.get(question=main_question)
                response_data = {
                    'message': 'Login successful',
                    'question_paper_details': question_paper_details,
                    'q_image': question_image.image.url
                }
            
                return JsonResponse(response_data)
            except QuestionPaper.DoesNotExist:
                return JsonResponse({'error': 'No exam scheduled for today or for this department'}, status=405)
            except QuestionImage.DoesNotExist:
                return JsonResponse({'error': 'Question image not found'}, status=403)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)


        
        
class Answers(APIView):

    def post(self ,request):
        data = request.data
        try:
            answer_serializer = AnswerSerializer(data = data)  
            if answer_serializer.is_valid():
                answer_serializer.save()
                return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
            else:   
                return JsonResponse(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    
    def get(self, request, *args, **kwargs):
        student_id = request.GET.get('studentId')
        question_code = request.GET.get('question')

       
        
        if not student_id and not question_code:
            answers = Answer.objects.all()
            answerdetails = [{

                'answer_id' : answer.id,
                'studentId': answer.student_id,
                'roll_number' : answer.student.roll_no,
                'question': answer.question_id,
                'question_code': answer.question.questioncode,
                'date': answer.date,
                'answerData': answer.answer_data,
                
            } for answer in answers]
            
            return JsonResponse({'data': answerdetails})
        
        
       
        
        

   
    
class StudentApplicationLogin(APIView):

    def post(self , request , *args , **kwargs):
        try:
            roll_no  = request.data.get('roll_no')
            password = request.data.get('dob')

           

            try:
                user = Student.objects.get(roll_no = roll_no , dob = password)

            except Student.DoesNotExist:
                user = None
           
            
            if user is not None :
                return JsonResponse({'message': 'Login successful'})
            
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class EvaluationLogin(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')


        try:
            teacher = Teacher.objects.get(email=email)
            teacher_id=teacher.id
            if not check_password(password, teacher.password):
                return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            assigned_evaluations = AssignEvaluation.objects.filter(teacher=teacher)
            print(assigned_evaluations)
            if not assigned_evaluations:
             return JsonResponse({'error': 'No assigned evaluations'}, status=status.HTTP_404_NOT_FOUND)
            answer_details = []
            

            for evaluation in assigned_evaluations:
               
                student_roll_nos = json.loads(evaluation.students)
                if not student_roll_nos:
                 return JsonResponse({'error': 'No students found'}, status=status.HTTP_404_NOT_FOUND)
                subject_id = evaluation.subject
   
                students = Student.objects.filter(roll_no__in=student_roll_nos)
                student_ids = students.values_list('id', flat=True)
                answers = Answer.objects.filter(student_id__in=student_ids, question__questionpaper__subject_id=subject_id)

                if not answers:
                 return JsonResponse({'error': 'No answers found'}, status=status.HTTP_404_NOT_FOUND)


                for answer in answers:
                    question_id = answer.question
                    question = QuestionImage.objects.get(question =question_id )
                    question_image = question.image.url
                    questionpaper_id        =  answer.question.questionpaper
                    blueprint               =  Blueprint.objects.get(question_paper = questionpaper_id)
                    total_questions = int(blueprint.total_questions)




                    answer_details.append({

                        'studentId': answer.student_id,
                        'answer_id':answer.id,
                        'answer_data': answer.answer_data,
                        'date': answer.date,
                        'subject': answer.question.questionpaper.subject.subject,
                        'department': answer.student.department.department,
                        'question_image' : question_image , 
                        'total_questions' :total_questions,
                        'question_code':answer.question.questioncode,
                        'teacherid':teacher_id,
                        
                    })

                # if not answer_details:
                #  return JsonResponse({'error': 'No students found, no assigned evaluations, or no answers present'}, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse(answer_details, safe=False)

        except Teacher.DoesNotExist:
            return JsonResponse({'error': 'Teacher not found'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class Evaluations(APIView):

    def post(self ,request):
          
          data = request.data
          evaluation_serializer = EvaluationSerializer(data = data)
          if evaluation_serializer.is_valid():
            evaluation_serializer.save()
            return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
          else:
              print(evaluation_serializer.errors)
              return JsonResponse(evaluation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
        

    
    def get(self, request):
        evaluations = Evaluation.objects.all().select_related(
            'answer__student', 
            'answer__question__questionpaper__subject', 
            'answer__question__questionpaper__department',
            'teacher'
        )

        evaluations_list = []

        for eval in evaluations:
            evaluations_list.append({
                'student_name': eval.answer.student.student_name if eval.answer.student else None,
                'subject_name': eval.answer.question.questionpaper.subject.subject if eval.answer.question.questionpaper.subject else None,
                'department_name': eval.answer.question.questionpaper.department.department if eval.answer.question.questionpaper.department else None,
                'teacher_name': eval.teacher.name if eval.teacher else None,
                'total_mark': eval.total_mark, 
                'date': eval.date,
            })

        return JsonResponse(evaluations_list, safe=False, status=status.HTTP_200_OK)

    def put(self, request,pk):
            data = request.data

            print(data ,"dataaaaaaaaaaaaaaa")
            id = data.get('id')
            evaluation = AssignEvaluation.objects.get(id=id)
        
            if 'department' in data:
                evaluation.department = data['department']
            if 'semester' in data:
                evaluation.semester = data['semester']
            if 'subject' in data:
                evaluation.subject = data['subject']
            if 'teacher' in data:
                evaluation.teacher = data['teacher']
            if 'endDate' in data:
                evaluation.endDate = data['endDate']
            if 'term' in data:
                evaluation.term = data['term']
            if 'students' in data:
                evaluation.students = data['students']
            evaluation.save()
            return JsonResponse({"message": "evaluation updated successfully"}, status=status.HTTP_200_OK)
       


    def delete(self, request, pk):
        try:
            evaluation = AssignEvaluation.objects.get(id=pk)
            evaluation.delete()
            return JsonResponse(status=status.HTTP_204_NO_CONTENT)
        except AssignEvaluation.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)

