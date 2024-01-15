from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app1.models import *
from app1.serializers import * 
from rest_framework.exceptions import ValidationError
from app1.token import get_token
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import login
from .serializers import *
from django.shortcuts import get_object_or_404
# from rest_framework.permissions import IsAuthenticated



class TeacherDetails(APIView):

    def get(self, request):
        teachers = Teacher.objects.all().order_by('id')
        
        teacherDetails = []

        for teacher in teachers:
            departments = teacher.departments.all()
            department_names = [department.department for department in departments]

            teacherDetails.append({
                'name': teacher.name,
                'departmentNames': department_names,  
                'contact': teacher.phoneNumber,
                'id'      : teacher.id
            })

        return JsonResponse(teacherDetails, safe=False)
    

    def delete(self , request , pk):
        try:
            teacher = Teacher.objects.get(id = pk)
            teacher.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)



class AssignBlueprint(APIView):

    def post(self , request):

        data = request.data
        questionpaper_serializer  = QuestionPaperSerializer(data = data)
        if questionpaper_serializer.is_valid():
            questionpaper_serializer.save(status='assigned')

            return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        
        else:
            return Response(questionpaper_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self , request):

        blueprints = QuestionPaper.objects.all().order_by('id')
        blueprintDetails = []

        for blueprint in blueprints:
            department_name = blueprint.department.department
            vetTeacher      = blueprint.vetTeacher1.name 
            blueprintDetails.append({

                'id'             :  blueprint.id,
                'ExamName'       :  blueprint.examName,
                'department'     :  department_name,
                'exam_date'       :  blueprint.exam_date,
                'semester'       :  blueprint.semester,
                'term'           :  blueprint.term,
                'status'         :  blueprint.status,
                'vetTeacher'     :  vetTeacher
            })

        return JsonResponse(blueprintDetails, safe=False)
    



        



# class BlueprintDetailAPI(APIView):
    # permission_classes = [IsAuthenticated]

    # def get(self, request, pk):
    #     question_paper = get_object_or_404(QuestionPaper, pk=pk)
    #     if request.user != question_paper.vetTeacher1.user:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     blueprint, created = Blueprint.objects.get_or_create(question_paper=question_paper)
    #     serializer = BlueprintSerializer(blueprint)
    #     return Response(serializer.data)

    # def put(self, request, pk):
    #     question_paper = get_object_or_404(QuestionPaper, pk=pk)
    #     if request.user != question_paper.vetTeacher1.user:
    #         return Response(status=status.HTTP_403_FORBIDDEN)
    #     blueprint = get_object_or_404(Blueprint, question_paper=question_paper)
    #     serializer = BlueprintSerializer(blueprint, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         question_paper.status = 'submitted'
    #         question_paper.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# class BlueprintReviewAPI(APIView):
    # permission_classes = [IsAdminUser]
    # def post(self, request, pk):
    #     question_paper = get_object_or_404(QuestionPaper, pk=pk)
    #     action = request.data.get('action')
    #     if action == 'approve':
    #         question_paper.status = 'approved'
    #     elif action == 'decline':
    #         question_paper.status = 'declined'
    #     else:
    #         return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)
    #     question_paper.save()
    #     return Response({'status': question_paper.status})


class BlueprintDetailView(APIView):

    def get(self, request, id):
        try:
            qpaper = QuestionPaper.objects.get(id=id)
            serializer = QuestionPaperSerializer(qpaper)  
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        except QuestionPaper.DoesNotExist:
            return JsonResponse({"detail": "Blueprint not found"}, status=status.HTTP_404_NOT_FOUND)
        

class TeacherLoginView(APIView):

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        try:
            teacher = Teacher.objects.get(email=email)
            teacher_id = teacher.id
        except Teacher.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        if teacher is not None and check_password(password, teacher.password):
            teacher_token = get_token(teacher, user_type='teacher')
            
            try:
                qpaper_assigned = QuestionPaper.objects.get(vetTeacher1_id=teacher_id)
                qpaper_details = qpaper_assigned

              
                response_data = {
                    'message': 'Login successful',
                    'token': teacher_token,
                    'qpaper_details': {
                        'id'      : qpaper_details.id,
                        'examName': qpaper_details.examName,
                        'department': qpaper_details.department.department,
                        'subject': qpaper_details.subject.subject,
                        'semester': qpaper_details.semester,
                        'total_time': qpaper_details.total_time,
                        'exam_date': qpaper_details.exam_date,
                        'vetTeacher1': qpaper_details.vetTeacher1.name,
                        'teacherid'  : qpaper_details.vetTeacher1.id,
                        'term': qpaper_details.term,
                        'status': qpaper_details.status,
                    }
                }
                return JsonResponse(response_data)
            except QuestionPaper.DoesNotExist:
                return JsonResponse({'message': 'Login successful', 'token': teacher_token})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        


class QpaperModule(APIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        blueprintSerializer = BlueprintSerializer(data = data)

        if blueprintSerializer.is_valid():
            
            blueprint_instance = blueprintSerializer.save()

            question_paper_instance = blueprint_instance.question_paper
            question_paper_instance.status = 'submitted'
            question_paper_instance.save()

            return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(blueprintSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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

    
    def put(self, request, qpaperid):
        try:
            question_paper = QuestionPaper.objects.get(pk=qpaperid)
        except QuestionPaper.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        data = request.data
        status_action = data.get('status_action', None)

        if status_action == "approve":
            question_paper.status = "approved"
            question_paper.save()
            return Response(status=status.HTTP_200_OK)
        elif status_action == "decline":
            question_paper.status = "declined"
            question_paper.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid status_action value"}, status=status.HTTP_400_BAD_REQUEST)
        


      

        
        
        