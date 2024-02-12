from rest_framework import status
from rest_framework.views import APIView
from app1.models import *
from aarna.models import *
from app1.serializers import * 
from aarna.models import * 
from rest_framework.exceptions import ValidationError
from app1.token import get_token
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import login
from .serializers import *
from django.shortcuts import get_object_or_404
from django.conf import settings
from datetime import datetime
import copy
from random import shuffle
import json

# from rest_framework.permissions import IsAuthenticated



class TeacherDetails(APIView):
    def get(self, request):
        try:
            teachers = Teacher.objects.all().order_by('id')

            teacherDetails = []

            for teacher in teachers:
                departments = teacher.departments.all()
                department_names = [department.department for department in departments]

                if teacher.image:
                    image_url = request.build_absolute_uri(settings.MEDIA_URL + str(teacher.image))
                else:
                    image_url = None

                teacherDetails.append({
                    'name': teacher.name,
                    'departmentNames': department_names,  
                    'contact': teacher.phoneNumber,
                    'id'      : teacher.id,
                    'image'   : image_url
                })

            return JsonResponse(teacherDetails, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self , request , pk):
        try:
            teacher = Teacher.objects.get(id=pk)
            teacher.delete()
            return JsonResponse(status=status.HTTP_204_NO_CONTENT)
        except Teacher.DoesNotExist:
            return JsonResponse({"detail": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle other unexpected errors
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    



class AssignBlueprint(APIView):

    def post(self , request):
        try:

            data = request.data
            questionpaper_serializer  = QuestionPaperSerializer(data = data)
            if questionpaper_serializer.is_valid():
                questionpaper_serializer.save(status='assigned')

                return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
            
            else:
                return JsonResponse(questionpaper_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle other unexpected errors
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

    def get(self , request):
        try:

            blueprints = QuestionPaper.objects.all().order_by('id')
            blueprintDetails = []

            for blueprint in blueprints:
                department_name = blueprint.department.department
                if blueprint.teacher is not None:
                    vetTeacher = blueprint.teacher.name
                else:
                    vetTeacher = "No Teacher Assigned"

                blueprintDetails.append({

                    'id'             :  blueprint.id,
                    'ExamName'       :  blueprint.exam_name,
                    'department'     :  department_name,
                    'exam_date'      :  blueprint.exam_date,
                    'semester'       :  blueprint.semester,
                    'term'           :  blueprint.term,
                    'status'         :  blueprint.status,
                    'vetTeacher'     :  vetTeacher,
                    'time'           :  blueprint.total_time
                })

            return JsonResponse(blueprintDetails, safe=False)
        except Exception as e:
            # Handle other unexpected errors
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    



class BlueprintDetailView(APIView):

    def get(self, request, id):
        try:
            qpaper = QuestionPaper.objects.get(id=id)
            serializer = QuestionPaperSerializer(qpaper)  
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except QuestionPaper.DoesNotExist:
            return JsonResponse({"detail": "Blueprint not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Handle other unexpected errors
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class TeacherLoginView(APIView):


        def post(self, request, *args, **kwargs):
            try:
                email = request.data.get('email')
                password = request.data.get('password')

            

                try:
                    teacher = Teacher.objects.get(email=email)
                    teacher_id = teacher.id
                except Teacher.DoesNotExist:
                    return JsonResponse({'error': 'Invalid email or password'}, status=401)

                if teacher is not None and check_password(password, teacher.password):
                    teacher_token = get_token(teacher, user_type='teacher')
                    
                    # try:
                        # qpaper_assigned = QuestionPaper.objects.get(teacher_id=teacher_id)
                    qpaper_assigned=QuestionPaper.objects.all()
                    question_paper_images      = QuestionImage.objects.all()
                    qpaper_detail = []

                    question_paper = []

                    for   question_paper_image in   question_paper_images :

                        question_paper.append({
                            'question_id' : question_paper_image.id,
                            'question' : question_paper_image.image.url

                        })

                    for qpaper_details in qpaper_assigned:
                        qpaper_detail.append({

                        'id'      : qpaper_details.id,
                        'examName': qpaper_details.exam_name,
                        'department': qpaper_details.department.department,
                        'subject': qpaper_details.subject.subject,
                        'semester': qpaper_details.semester,
                        'total_time': qpaper_details.total_time,
                        'exam_date': qpaper_details.exam_date,
                        'vetTeacher1': qpaper_details.teacher.name,
                        'teacherid'  : qpaper_details.teacher.id,
                        'term': qpaper_details.term,
                        'status': qpaper_details.status,
                        
                        }
                        )

                        

                    response_data = {
                        'message': 'Login successful',
                        'token': teacher_token,
                        'qpaper_detail': qpaper_detail,
                        'question_paper' : question_paper,
                    
                        # 'qpaper_details': {
                        #     # 'id'      : qpaper_details.id,
                        #     'examName': qpaper_details.exam_name,
                        #     'department': qpaper_details.department.department,
                        #     'subject': qpaper_details.subject.subject,
                        #     'semester': qpaper_details.semester,
                        #     'total_time': qpaper_details.total_time,
                        #     'exam_date': qpaper_details.exam_date,
                        #     'vetTeacher1': qpaper_details.teacher.name,
                        #     'teacherid'  : qpaper_details.teacher.id,
                        #     'term': qpaper_details.term,
                        #     'status': qpaper_details.status,
                        # }
                    }
                    return JsonResponse(response_data)
                    # except QuestionPaper.DoesNotExist:
                    #     return JsonResponse({'message': 'Login successful', 'token': teacher_token})
                else:
                    return JsonResponse({'error': 'Invalid credentials'}, status=401)
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class QpaperModule(APIView):

    def post(self, request, *args, **kwargs):
        try: 
                data = request.data
                blueprintSerializer = BlueprintSerializer(data = data)

                if blueprintSerializer.is_valid():
                    
                    blueprint_instance = blueprintSerializer.save()

                    question_paper_instance = blueprint_instance.question_paper
                    question_paper_instance.status = 'submitted'
                    question_paper_instance.save()

                    return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
                else:
                    return JsonResponse(blueprintSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

    def get(self, request, qpaperid,*args, **kwargs ):
        try:
            blueprints    = Blueprint.objects.get(question_paper_id = qpaperid)
            qpaper_status = blueprints.question_paper.status
            serializer = BlueprintSerializer(blueprints)  
            data = serializer.data
            data["qpaper_status"] = qpaper_status
            return JsonResponse(data, status=status.HTTP_200_OK )
        except Blueprint.DoesNotExist:
            return JsonResponse({"detail": "Blueprint not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
                return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request, qpaperid):
        try:
            question_paper = QuestionPaper.objects.get(pk=qpaperid)
        except QuestionPaper.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)
        data = request.data
        status_action = data.get('status_action', None)
       
        if status_action == "approve":
            question_paper.status = "approved"
            question_paper.save()

            TimeTable.objects.get_or_create(
                exam_name=question_paper.exam_name,
                department=question_paper.department,
                subject_id=question_paper.subject_id,
                exam_date=question_paper.exam_date,
                exam_time=question_paper.total_time
            )
            return JsonResponse({'message':'QuestionPaper approved successfully'},status=status.HTTP_200_OK)
        elif status_action == "decline":
            question_paper.status = "declined"
            question_paper.save()

            Blueprint.objects.filter(question_paper=qpaperid).delete()

            return JsonResponse({'message': 'QuestionPaper declined successfully'},status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "Invalid status_action value"}, status=status.HTTP_400_BAD_REQUEST)
        
    
        


# .values_list('id', flat=True)



    

    
        

        

        
    

        
        
        