from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from app1.models import *
from aarna.models import *
from app1.serializers import *
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from flutter.models import *
from .serializers import *
from django.db import transaction
from django.db.models import Q
from rest_framework import status
from datetime import datetime




class AddStudent(APIView):
   
  def post(self, request):
    mobile_number = request.data.get('number')
    roll_no = request.data.get('roll_no')
  
    if Student.objects.filter(number=mobile_number).exists():
        return Response({'message': 'A student with the same mobile number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if Student.objects.filter(roll_no=roll_no).exists():
        return Response({'message': 'A student with the same register number already exists.'}, status=status.HTTP_400_BAD_REQUEST)

    student_serializer = StudentSerializer(data=request.data)
    if student_serializer.is_valid():
        student_serializer.save()
        return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
class StudentExaminationLogin(APIView):
    def post(self, request, *args, **kwargs):
        roll_no = request.data.get('roll_no')
        password = request.data.get('password')

        try:
            user = Student.objects.get(roll_no=roll_no)

           
            if user is not None and check_password(password, user.password):
                current_date = datetime.now().date()
                department_id = user.department_id
                

                try:
                    questionpaper = QuestionPaper.objects.get(department_id=department_id, exam_date=current_date)
                    main_question = Questions.objects.filter(questionpaper=questionpaper).first()

                    print( main_question.questioncode,"question code")
                    

                
                    question_paper_details = {
                        'student_id':user.id,
                        'exam_name': questionpaper.exam_name,
                        'total_time': questionpaper.total_time,
                        'semester': questionpaper.semester,
                        'department': questionpaper.department.department,  
                        'subject': questionpaper.subject.subject, 
                        'subject_code': questionpaper.subject.subject_code, 
                        'teacher': questionpaper.teacher.name,  
                        'question_id' : main_question.id,
                        'question_code'      : main_question.questioncode ,
                        # 'total_questions'    : total_compulsory_questions
                        

                    }


                   
                    if main_question:
                        try:

                            question_image = QuestionImage.objects.get(question=main_question)
                            question_image_data = question_image.image.url

                            response_data = {
                                'message': 'Login successful',
                                'question_paper_details': question_paper_details,
                                'q_image': question_image_data
                            }
                            return JsonResponse(response_data)

                        except QuestionImage.DoesNotExist:
                            return JsonResponse({'error': 'Question image not found'}, status=403)
                    else:
                        return JsonResponse({'error': 'No questions found for the exam'}, status=405)

                except QuestionPaper.DoesNotExist:
                    return JsonResponse({'error': 'No exam scheduled for today'}, status=410)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
        
        
class Answers(APIView):

    def post(self ,request):
        data = request.data

        answer_serializer = AnswerSerializer(data = data)  
        if answer_serializer.is_valid():
            answer_serializer.save()
            return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:   
            return JsonResponse(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request, *args, **kwargs):
        student_id = request.GET.get('studentId')
        question_code = request.GET.get('question')
        print(student_id, 'student_id is hereeeee')
        print(question_code, 'question_code is hereeeee')
        
        # if not student_id and not question_code:
        answers = Answer.objects.all()
        print(answers,"answersssssss")
        
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
        
        # if not student_id:
        #     return JsonResponse({'error': 'Student ID is required'}, status=400)
            
        # if not question_code:
        #     answers = Answer.objects.filter(studentId=student_id)
        #     answerdetails = [{
        #         'studentId': answer.student,
        #         'question': answer.question,
        #         'date': answer.date,
        #         'answerData': answer.answer_data,
        #     } for answer in answers]
            
        #     return JsonResponse({'data': answerdetails})
        # else:
        #     try:
        #         answer = Answer.objects.get(studentId=student_id, question=question_code)
        #         print(answer, 'answer is hereeeee')
        #         return JsonResponse({'data': answer.answer_data})
        #     except Answer.DoesNotExist:
        #         return JsonResponse({'error': 'No matching record found'}, status=404)
        
        
class Evaluations(APIView):

    def post(self ,request):
       
        data = request.data

        print(data,"aaaaaaaaaa")

        evaluation_serializer = EvaluationSerializer(data = data)

        print(evaluation_serializer,"aaaaaaaaaaaaaaaaaa")
      

        if evaluation_serializer.is_valid():
            evaluation_serializer.save()
        
            return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            print(evaluation_serializer.errors,"errorrrrssssssssssssss")
            return JsonResponse(evaluation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self , request):

        evaluations = Evaluation.objects.all()

        answerdetails = []

        for evaluation in evaluations:
            answerdetails.append({
                'studentId':evaluation.answer.student.studentName ,
                # 'teacherId':evaluation.teacher,
                'markData':evaluation.mark_data,
                'totalMark':evaluation.total_mark,
                'date':evaluation.date,
                'subject' : evaluation.answer.question.questionpaper.subject.subject,
                'department' : evaluation.answer.student.department.department
            })
        

        return JsonResponse(answerdetails, safe=False)



class StudentApplicationLogin(APIView):

    def post(self , request , *args , **kwargs):
        roll_no  = request.data.get('roll_no')
        password = request.data.get('dob')

        try:
            user = Student.objects.get(roll_no = roll_no , dob = password)

        except Student.DoesNotExist:
            user = None
        # if user is not None and check_password(password,user.password):
        #     return JsonResponse({'message': 'Login successful'})
        
        if user is not None :
            return JsonResponse({'message': 'Login successful'})
        
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        



