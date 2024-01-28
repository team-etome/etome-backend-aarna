from rest_framework import status
from rest_framework.response import Response
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
            print(questionpaper_serializer.errors ,"aaaaaaaaaaaa")
            return Response(questionpaper_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self , request):

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
                qpaper_assigned = QuestionPaper.objects.get(teacher_id=teacher_id)
                qpaper_details = qpaper_assigned

              
                response_data = {
                    'message': 'Login successful',
                    'token': teacher_token,
                    'qpaper_details': {
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
        print(status_action,"status action")
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
            return Response(status=status.HTTP_200_OK)
        elif status_action == "decline":
            question_paper.status = "declined"
            question_paper.save()

            Blueprint.objects.filter(question_paper=qpaperid).delete()

            return Response(status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid status_action value"}, status=status.HTTP_400_BAD_REQUEST)
    
        


class SeatingArrangementView(APIView):
    
    def patterned_distribution(self, dept_students, rows, cols, students_per_bench):
      
        assert all(len(students) >= students_per_bench for students in dept_students.values())
        seating_arrangement = []
        dept_keys = list(dept_students.keys())
        total_depts = len(dept_keys)

        for bench_num in range(rows * cols):
            bench_students = []
            for student_num in range(students_per_bench):
                dept_index = (bench_num + student_num) % total_depts
                dept_key = dept_keys[dept_index]
                if dept_students[dept_key]:
                    bench_students.append(dept_students[dept_key].pop(0))
            seating_arrangement.append(bench_students)

        return seating_arrangement

    def sequential_distribution(self, dept_students, rows, cols, students_per_bench):
        seating_arrangement = []
        max_students_per_dept = max(len(students) for students in dept_students.values())

        for bench_num in range(rows * cols):
            bench_students = []
            for dept_key in dept_students.keys():
                student_num = bench_num // cols
                if student_num < len(dept_students[dept_key]):
                    bench_students.append(dept_students[dept_key][student_num])
                else:
                    # Add None for empty seats
                    bench_students.append(None) 

            seating_arrangement.append(bench_students)

        return seating_arrangement


    def post(self, request, *args, **kwargs):
        data = request.data
        print(data,"bbbbbbbbbbbbbbbbbbbbbbbbbbb")
        pattern_type = data.get('seating_layout')
        pattern      = data.get('pattern')
        print(pattern_type,"aaaaaaaaaaaaaaaaaaaaaaaaaa")
        department_ids = [int(id) for id in data.get('departments', []) if id.isdigit()]
        students = Student.objects.filter(department__id__in=department_ids, selected=False)

        department_students = {}
        for student in students:
            dept_id = student.department.id
            if dept_id not in department_students:
                department_students[dept_id] = []
            department_students[dept_id].append(student.roll_no)

        print(department_students  , "department students 1")
        
      
        hall_name = data.get('hallName')
        teacher_id = data.get('teacher')
        exam_name = data.get('exam_name')
        exam_date = data.get('exam_date')
        exam_time = data.get('exam_time')
        seating_layout = data.get('seating_layout')
        teacher_id = data.get('teacher')[0] if data.get('teacher') else None

        rows = int(data.get('rows'))
        cols = int(data.get('cols'))
        students_per_bench = int(data.get('studentsPerBench'))

      
        exam_date_obj = datetime.strptime(exam_date, '%Y-%m-%d').date()
   
        if pattern_type == 'patterned':
            # Clone the dictionary before passing to the function
            cloned_dept_students = copy.deepcopy(department_students)
            seating_arrangement = self.patterned_distribution(cloned_dept_students, rows, cols, students_per_bench)
        elif pattern_type == 'sequential':
            # Similarly, clone for the sequential distribution
            cloned_dept_students = copy.deepcopy(department_students)
            seating_arrangement = self.sequential_distribution(cloned_dept_students, rows, cols, students_per_bench)
        else:
            return Response({'error': 'Invalid pattern type provided.'}, status=status.HTTP_400_BAD_REQUEST)



        print(department_students  , "department students 2")
      
        SeatingArrangement.objects.create(
            pattern=pattern,
            hall_name=hall_name,
            teacher_id=teacher_id,
            exam_name=exam_name,
            exam_date=exam_date_obj,
            exam_time=exam_time,
            seating_layout=seating_layout,
            department_students=department_students
        )

        selected_student_ids = [student.id for student in students]
        Student.objects.filter(id__in=selected_student_ids).update(selected=True)

        

        return Response({'seating_arrangement': seating_arrangement}, status=status.HTTP_200_OK)
    

    def get(self, request):

        print("enteredddddddddddddd")

        seating_arrangements = SeatingArrangement.objects.all().order_by('id')

        print(seating_arrangements,'aaaaaaaaaaaaaaaaaaaa')

        exam_names = [seating.exam_name for seating in seating_arrangements]

        question_papers = QuestionPaper.objects.filter(exam_name__in=exam_names)

        term_data = [paper.term for paper in question_papers]

        seatingDetails = []

        total_student_count = 0
        total_department_count = 0


        for seating in seating_arrangements:

           
            department_students = seating.department_students
            student_count = sum(len(student_list) for student_list in department_students.values())
            total_student_count += student_count
            department_count = len(department_students)
            total_department_count += department_count
            department_id = list(department_students.keys())[0]

            if department_students:
                department_id = list(department_students.keys())[0]
                department = Department.objects.get(id=department_id)  
                department_code = department.department_code
            else:
                department_code = 'N/A'

            detail = {

                'hall_name': seating.hall_name,
                'teacher': seating.teacher.name,
                'term_data': term_data,
                'student_count': student_count,
                'department_count': department_count,
                'department_code': department_code
            }

            seatingDetails.append(detail)

            print(seatingDetails,'seating detailssss')


        return JsonResponse(seatingDetails, safe=False)

        

        
    

        
        
        