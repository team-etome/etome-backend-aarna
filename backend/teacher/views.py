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
from django.conf import settings
# from rest_framework.permissions import IsAuthenticated



class TeacherDetails(APIView):

    def get(self, request):
        teachers = Teacher.objects.all().order_by('id')
        
        teacherDetails = []

        for teacher in teachers:
            departments = teacher.departments.all()
            department_names = [department.department for department in departments]

            if teacher.image:
                image_url = request.build_absolute_uri(settings.MEDIA_URL + str(teacher.image))
                print(image_url,"image urllll")
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
                'vetTeacher'     :  vetTeacher,
                'time'           :  blueprint.total_time
            })

        return JsonResponse(blueprintDetails, safe=False)
    



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
        


class SeatingArrangementView(APIView):
    
    def patterned_distribution(self, dept_students, rows, cols, students_per_bench):
        # Check there are enough students in each department list
        assert all(len(students) >= students_per_bench for students in dept_students.values())

        # Create the seating arrangement following the provided pattern
        seating_arrangement = []
        dept_keys = list(dept_students.keys())
        total_depts = len(dept_keys)

        for bench_num in range(rows * cols):
            bench_students = []
            for student_num in range(students_per_bench):
                # Calculate department index (cycle through departments)
                dept_index = (bench_num + student_num) % total_depts
                # Get the department key based on current index
                dept_key = dept_keys[dept_index]
                # Append the student to the bench list and remove from department list
                if dept_students[dept_key]:
                    bench_students.append(dept_students[dept_key].pop(0))
            # Add the bench list to the seating arrangement
            seating_arrangement.append(bench_students)

        return seating_arrangement

    def sequential_distribution(self, dept_students, rows, cols, students_per_bench):
        # Ensure there are enough students in each list for the seating arrangement
        assert all(len(students) >= rows for students in dept_students.values())

        # Create the seating arrangement following the sequential pattern
        seating_arrangement = []
        for bench_num in range(rows * cols):
            bench_students = []
            for dept_key in dept_students.keys():
                # Get the student number based on the row
                student_num = bench_num // cols
                # Assign the student to the bench
                if student_num < len(dept_students[dept_key]):
                    bench_students.append(dept_students[dept_key][student_num])
                else:
                    bench_students.append(None)  # Append None if there are no more students
            # Add the bench list to the seating arrangement
            seating_arrangement.append(bench_students)

        return seating_arrangement

    def post(self, request, *args, **kwargs):
        # Extract data from request.data
        pattern_type = request.data.get('pattern_type')
        dept_students = {
            'A': request.data.get('A_students'),
            'B': request.data.get('B_students'),
            'C': request.data.get('C_students'),
        }
        rows = request.data.get('rows')
        cols = request.data.get('cols')
        students_per_bench = request.data.get('students_per_bench')

        # Validate input data here

        # Check for valid pattern type and call the appropriate distribution function
        if pattern_type == 'patterned':
            seating_arrangement = self.patterned_distribution(dept_students, rows, cols, students_per_bench)
        elif pattern_type == 'sequential':
            seating_arrangement = self.sequential_distribution(dept_students, rows, cols, students_per_bench)
        else:
            # Handle invalid pattern type
            return Response({'error': 'Invalid pattern type provided.'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            'seating_arrangement': seating_arrangement
        }, status=status.HTTP_200_OK)



        
        
        