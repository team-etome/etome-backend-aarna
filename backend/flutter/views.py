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

    student_serializer = StudentSerializer(data=request.data)
    if student_serializer.is_valid():
        student_serializer.save()
        return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse(student_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

       
   
class StudentExaminationLogin(APIView):
    def post(self, request, *args, **kwargs):
        roll_no = request.data.get('roll_no')
        password = request.data.get('password')

        try:
            user = Student.objects.get(roll_no=roll_no)
            if user is not None and check_password(password, user.password):
                current_datetime = datetime.now() 
                department_id = user.department_id

                try:
                    questionpaper = QuestionPaper.objects.get(department_id=department_id, exam_date=current_datetime.date())
                    questionpaper_id=questionpaper.id
                    main_question = Questions.objects.filter(questionpaper=questionpaper).first()
                    blueprint  = Blueprint.objects.get(question_paper =questionpaper_id )
                    print(blueprint.total_questions)
                    total_questions = int(blueprint.total_questions)


                    if not main_question:
                        return JsonResponse({'error': 'No questions found for the exam'}, status=405)

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
                        'total_question':total_questions
                    }
                    question_image = QuestionImage.objects.get(question=main_question)
                    response_data = {
                        'message': 'Login successful',
                        'question_paper_details': question_paper_details,
                        'q_image': question_image.image.url
                    }
                    return JsonResponse(response_data)
                except QuestionPaper.DoesNotExist:
                    return JsonResponse({'error': 'No exam scheduled for today or for this department'}, status=404)
                except QuestionImage.DoesNotExist:
                    return JsonResponse({'error': 'Question image not found'}, status=403)
            else:
                return JsonResponse({'error': 'Invalid credentials'}, status=401)

        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)
        
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

        # print(student_id , question_code , "studentsssssssssssssssssssssssssss")

        # if not student_id:
        #     return JsonResponse({'error': 'Student ID is required'}, status=400)
        
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
        
        

   
    # def get(self , request):
    #     try:

    #         evaluations = Evaluation.objects.all()

    #         answerdetails = []

    #         for evaluation in evaluations:
    #             answerdetails.append({
    #                 'studentId':evaluation.answer.student.studentName ,
    #                 # 'teacherId':evaluation.teacher,
    #                 'markData':evaluation.mark_data,
    #                 'totalMark':evaluation.total_mark,
    #                 'date':evaluation.date,
    #                 'subject' : evaluation.answer.question.questionpaper.subject.subject,
    #                 'department' : evaluation.answer.student.department.department
    #             })
            

    #         return JsonResponse(answerdetails, safe=False)
    #     except Exception as e:
    #         return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





class StudentApplicationLogin(APIView):

    def post(self , request , *args , **kwargs):
        try:
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
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



class EvaluationLogin(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        print(email,password,".........................")


        try:
            teacher = Teacher.objects.get(email=email)
            teacher_id=teacher.id
            print(teacher)
            if not check_password(password, teacher.password):
                return JsonResponse({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

            assigned_evaluations = AssignEvaluation.objects.filter(teacher=teacher)
            print(assigned_evaluations)
            if not assigned_evaluations:
             return JsonResponse({'error': 'No assigned evaluations'}, status=status.HTTP_404_NOT_FOUND)
            answer_details = []
            

            for evaluation in assigned_evaluations:
               
                student_roll_nos = json.loads(evaluation.students)
                print(student_roll_nos)
                if not student_roll_nos:
                 return JsonResponse({'error': 'No students found'}, status=403)
                subject_id = evaluation.subject
                print(subject_id)
   
                students = Student.objects.filter(roll_no__in=student_roll_nos)
                print(students)
                # if not students:
                #  return JsonResponse({'error': 'No students found'}, status=status.HTTP_404_NOT_FOUND)
                student_ids = students.values_list('id', flat=True)
                print(student_ids,"ssssssssssssssssssssssssssssssss")
                # print(Answer.objects.get( 'question__questionpaper__subject_id'))
                answers = Answer.objects.filter(student_id__in=student_ids, question__questionpaper__subject_id=subject_id)

                if not answers:
                 return JsonResponse({'error': 'No answers found'}, status=status.HTTP_404_NOT_FOUND)
                print(answers , 'answersssssssssssssssssssssssssssssss')


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

                if not answer_details:
                 return JsonResponse({'error': 'No students found, no assigned evaluations, or no answers present'}, status=status.HTTP_404_NOT_FOUND)
                print(answer_details,"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")


            return JsonResponse(answer_details, safe=False)

        except Teacher.DoesNotExist:
            return JsonResponse({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        # except AssignEvaluation.DoesNotExist:
        #     return JsonResponse({'error': 'no evaluation exists'}, status=403)
        # except Student.DoesNotExist:
        #     return JsonResponse({'error': 'no student exists'}, status=401)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class Evaluations(APIView):

    def post(self ,request):

        # try:
          data = request.data
          answer_id=type(request.data.get('answer'))
          print(data,answer_id,"aaaaaaaaaaaaaaaaaaaaaaaaaaa")
          evaluation_serializer = EvaluationSerializer(data = data)
          if evaluation_serializer.is_valid():
            evaluation_serializer.save()
            return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
          else:
              print(evaluation_serializer.errors,"eeeeeeeeeeeeeeeeeeeeeeeee")
              return JsonResponse(evaluation_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    
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
                'student_name': eval.answer.student.studentName if eval.answer.student else None,
                'subject_name': eval.answer.question.questionpaper.subject.subject if eval.answer.question.questionpaper.subject else None,
                'department_name': eval.answer.question.questionpaper.department.department if eval.answer.question.questionpaper.department else None,
                'teacher_name': eval.teacher.name if eval.teacher else None,
                'total_mark': eval.total_mark,  # Add total_mark
                'date': eval.date,
            })

        return JsonResponse(evaluations_list, safe=False, status=status.HTTP_200_OK)


