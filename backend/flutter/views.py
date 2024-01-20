from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from app1.models import *
from app1.serializers import *
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from flutter.models import *
from .serializers import *
from django.db import transaction
from django.db.models import Q
from rest_framework import status




class AddStudent(APIView):
    def post(self , request ):
        print("Enterrrrrrr")
        data = request.data
        print(data,"qqqqqqqqqqqqqqqq")
        student_serializer = StudentSerializer(data = data)

        if student_serializer.is_valid():
            student_serializer.save()
            return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)




#Student Login
class StudentExaminationLogin(APIView):

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
            print("enterrrrrrrrrrrrrrr")
            return JsonResponse({'message': 'Login successful'})
        
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        
class Answers(APIView):
    def post(self ,request):
        print('enterrrrrrrrrrrrrrrr')
        data = request.data
        answer_serializer = AnswerSerializer(data = data)
        print(answer_serializer,'serializer')
        if answer_serializer.is_valid():
            print('reached 1')
            answer_serializer.save()
            return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            print(answer_serializer.errors, 'errorrrrrr')
            return JsonResponse(answer_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self, request, *args, **kwargs):
        student_id = request.GET.get('studentId')
        question_code = request.GET.get('questionCode')
        print(student_id,'student_id is hereeeee')
        print(question_code,'question_code is hereeeee')
        if not student_id or not question_code:
            print("giving all answer data")
            answers = Answer.objects.all()
            answerdetails = []
            for answer in answers:
                answerdetails.append({
                    'studentId':answer.studentId,
                    'questionCode':answer.questionCode,
                    'date':answer.date,
                    'answerData':answer.answerData,
                })
            return JsonResponse({'data': answerdetails}, status=400)
        try:
            answer = Answer.objects.get(studentId=student_id, questionCode=question_code)
            print(answer,'answer is hereeeee')
            return JsonResponse({'data': answer.answerData})
        except Answer.DoesNotExist:
            return JsonResponse({'error': 'No matching record found'}, status=404)
        

      
        


        # answerdetails = []
        # if answer:
        #     answerdetails = {
        #     'studentId': answer.studentId,
        #     'questionCode': answer.questionCode,
        #     'date': answer.date,
        #     'answerData': answer.answerData,
        #     }
        # return JsonResponse(answerdetails, safe=False)
        
class Evaluations(APIView):

    def post(self ,request):
        print('enterrrrrrrrrrrrrrrr')
        data = request.data
        print(data,'dataaaaaaaaaa')
        evaluation_serializer = EvaluationSerializer(data = data)
        print(evaluation_serializer,'serializer')

        if evaluation_serializer.is_valid():
            print('reached 1')
            evaluation_serializer.save()
        
            return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            print(evaluation_serializer.errors, 'errorrrrrr')
            return JsonResponse(evaluation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    
    def get(self , request):

        answers = Evaluation.objects.all()

        answerdetails = []

        for answer in answers:
            answerdetails.append({
                'studentId':answer.studentId,
                'questionCode':answer.questionCode,
                'teacherId':answer.teacherId,
                'markData':answer.markData,
                'totalMark':answer.totalMark,
                'date':answer.date,
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
