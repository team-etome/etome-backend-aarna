from rest_framework import status
from rest_framework.views import APIView
from app1.models import *
from aarna.models import *
from app1.serializers import * 
from aarna.models import * 
from app1.token import get_token
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .serializers import *
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
                try:
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
                        'id': teacher.id,
                        'image': image_url
                    })
                except Exception as e:
                    return JsonResponse("Error processing details for teacher with ID ")

            return JsonResponse(teacherDetails, safe=False)

        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {e}"}, status=500)



    def delete(self , request , pk):
        try:
            teacher = Teacher.objects.get(id=pk)
            teacher.delete()
            return JsonResponse({'message': 'Teacher deleted successfully'},status=status.HTTP_204_NO_CONTENT)
        except Teacher.DoesNotExist:
            return JsonResponse({'error': 'Teacher not found'}, status=status.HTTP_404_NOT_FOUND)
        
        except Exception as e:
            return JsonResponse({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



class AssignBlueprint(APIView):

    def post(self , request):

        data = request.data
        questionpaper_serializer  = QuestionPaperSerializer(data = data)
        if questionpaper_serializer.is_valid():
            questionpaper_serializer.save(status='assigned')

            return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        
        else:
            return JsonResponse(questionpaper_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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
                'start_time'     :  blueprint.start_time , 
                'end_time'       :  blueprint.end_time
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
        except Exception as e:
            return JsonResponse({'error': f"An error occurred: {e}"}, status=500)        


# class TeacherLoginView(APIView):


#     def post(self, request, *args, **kwargs):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         try:
#           teacher = Teacher.objects.get(email=email)
#           teacher_id = teacher.id
#         except Teacher.DoesNotExist:
#                     return JsonResponse({'error': 'Invalid email or password'}, status=401)

#         if teacher is not None and check_password(password, teacher.password):
#             teacher_token = get_token(teacher, user_type='teacher')
            
#             try:
#                 qpapers_assigned = QuestionPaper.objects.filter(teacher_id=teacher_id)
#                 qpapers_details = []
#                 for qpaper_assigned in qpapers_assigned:
#                     qpaper_details = {
#                         'id': qpaper_assigned.id,
#                         'examName': qpaper_assigned.exam_name,
#                         'department': qpaper_assigned.department.department,
#                         'subject': qpaper_assigned.subject.subject,
#                         'semester': qpaper_assigned.semester,
#                         'total_time': qpaper_assigned.total_time,
#                         'exam_date': qpaper_assigned.exam_date,
#                         'vetTeacher1': qpaper_assigned.teacher.name,
#                         'teacherid': qpaper_assigned.teacher.id,
#                         'term': qpaper_assigned.term,
#                         'status': qpaper_assigned.status,
#                     }
#                     qpapers_details.append(qpaper_details)

#                 response_data = {
#                     'message': 'Login successful',
#                     'token': teacher_token,
#                     'qpaper_details': qpapers_details
#                 }
#                 return JsonResponse(response_data)
#             except QuestionPaper.DoesNotExist:
#                 return JsonResponse({'message': 'Login successful', 'token': teacher_token})
#         else:
#             return JsonResponse({'error': 'Invalid credentials'}, status=401)
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


                response_data = {
                    'message': 'Login successful',
                    'token': teacher_token,
                    'qpaper_details': {
                        'id'      : qpaper_assigned.id,
                        'examName': qpaper_assigned.exam_name,
                        'department': qpaper_assigned.department.department,
                        'subject': qpaper_assigned.subject.subject,
                        'semester': qpaper_assigned.semester,
                        'total_time': qpaper_assigned.total_time,
                        'exam_date': qpaper_assigned.exam_date,
                        'vetTeacher1': qpaper_assigned.teacher.name,
                        'teacherid'  : qpaper_assigned.teacher.id,
                        'term': qpaper_assigned.term,
                        'status': qpaper_assigned.status,
                    }
                }
                return JsonResponse(response_data)
            except QuestionPaper.DoesNotExist:
                return JsonResponse({'message': 'Login successful', 'token': teacher_token})
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)


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
        except:
            return JsonResponse(blueprintSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

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
            return JsonResponse({'error': f"An error occurred: {e}"}, status=500)

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
            return JsonResponse(data={},status=status.HTTP_200_OK)
        elif status_action == "decline":
            question_paper.status = "declined"
            question_paper.save()

            Blueprint.objects.filter(question_paper=qpaperid).delete()
            return JsonResponse(status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "Invalid status_action value"}, status=status.HTTP_400_BAD_REQUEST)

    
        
class SeatingArrangementView(APIView):
     
    def patterned_distribution(self,cols, rows, student_per_table, department_ids):

        if department_ids is None:
            department_ids = Department.objects.all().values_list('id', flat=True)
        department_codes_per_department = Department.objects.filter(id__in=department_ids).values('id', 'department_code')
        department_id_to_code = {dept['id']: dept['department_code'] for dept in department_codes_per_department}
        student_ids_per_department = {}
        for department_id in department_ids:
            student_ids = list(Student.objects.filter(department_id=department_id).order_by('roll_no').values_list('roll_no', flat=True))
            student_ids_per_department[department_id] = student_ids
        total_capacity_of_hall = student_per_table * rows
        departments = len(department_ids)
        department_labels = list(department_ids)
        shuffle(department_labels)
        total_students_from_each_department = total_capacity_of_hall // departments
        seating_arrangement = []
        vacant_seats = 0
        for t in range(rows):
            table = []
            for s in range(student_per_table):
               
                department_index = (t * student_per_table + s) % departments
                department_id = department_labels[department_index]
             
                department_code = department_id_to_code.get(department_id,"h")
               
                if student_ids_per_department[department_id]:
                    seat_label = f"{department_code}-{student_ids_per_department[department_id].pop(0)}"
                else:
                    seat_label = "Vacant-0"
                    vacant_seats += 1
                table.append(seat_label)

            seating_arrangement.append(table)
        columned_seating_arrangement = [seating_arrangement[i:i + cols] for i in range(0, len(seating_arrangement), cols)]

        return columned_seating_arrangement, vacant_seats
    

    def sequential_distribution(self, cols, rows, student_per_table, department_ids):
        if department_ids is None:
                department_ids = Department.objects.all().values_list('id', flat=True)
        department_codes_per_department = Department.objects.filter(id__in=department_ids).values('id', 'department_code')
        department_id_to_code = {dept['id']: dept['department_code'] for dept in department_codes_per_department}
        student_ids_per_department = {}
        for department_id in department_ids:
            student_ids = list(Student.objects.filter(department_id=department_id).order_by('roll_no').values_list('roll_no', flat=True))
            student_ids_per_department[department_id] = student_ids
        total_capacity_of_hall = student_per_table * rows
        departments = len(department_ids)
        department_labels = list(department_ids)
        shuffle(department_labels)
        total_students_from_each_department = total_capacity_of_hall // departments

        seating_arrangement = []
        vacant_seats = 0

        for t in range(rows):
            table = []
            for s in range(student_per_table):
                department_index = (t * student_per_table + s) % departments
                department_id = department_ids[department_index]
                department_code = department_id_to_code.get(department_id,"h")
                if student_ids_per_department[department_id]:
                    seat_label = f"{department_code}-{student_ids_per_department[department_id].pop(0)}"
                else:
                    seat_label = "Vacant-0"
                    vacant_seats += 1
                table.append(seat_label)
            seating_arrangement.append(table)
        columned_seating_arrangement = [seating_arrangement[i:i + cols] for i in range(0, len(seating_arrangement), cols)]
           

        return columned_seating_arrangement, vacant_seats

        
    def post(self, request, *args, **kwargs):
        data = request.data
        pattern_type = data.get('seating_layout')
        pattern      = data.get('pattern')
        department_ids = [int(id) for id in data.get('departments', [])]

        try:
         students = Student.objects.filter(department__id__in=department_ids , selected=False)
        except Student.DoesNotExist:
            return JsonResponse("Student not found")
      
        department_students = {}
        for student in students:
            dept_id = student.department.id
            if dept_id not in department_students:
                department_students[dept_id] = []
            department_students[dept_id].append(student.roll_no)

        
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
            cloned_dept_students = copy.deepcopy(department_students)
            seating_arrangement, vacant_seats = self.patterned_distribution(cols, rows, students_per_bench, department_ids)
            columned_seating_arrangement_json = json.dumps(seating_arrangement)
        elif pattern_type == 'sequential':

            # Similarly, clone for the sequential distribution
            cloned_dept_students = copy.deepcopy(department_students)
            seating_arrangement,vacant_seats = self.sequential_distribution(  cols,rows, students_per_bench,department_ids)
            columned_seating_arrangement_json = json.dumps(seating_arrangement)
        else:
            return JsonResponse({'error': 'Invalid pattern type provided.'}, status=status.HTTP_400_BAD_REQUEST)
        try:      
            SeatingArrangement.objects.create(
                pattern=pattern,
                hall_name=hall_name,
                teacher_id=teacher_id,
                exam_name=exam_name,
                exam_date=exam_date_obj,
                exam_time=exam_time,
                seating_layout=seating_layout,
                department_students=columned_seating_arrangement_json,
                department_ids=json.dumps(department_ids)
            )

            selected_student_ids = [student.id for student in students]
            Student.objects.filter(id__in=selected_student_ids).update(selected=True)


            
            return JsonResponse({'seating_arrangement': seating_arrangement}, status=status.HTTP_200_OK)
        except :
            return JsonResponse(seating_arrangement.errors, status=status.HTTP_400_BAD_REQUEST)

          
          
    def get(self, request):
        seating_arrangements = SeatingArrangement.objects.all().order_by('id')
        exam_names = [seating.exam_name for seating in seating_arrangements]
        question_papers = QuestionPaper.objects.filter(exam_name__in=exam_names)
        term_data = set(paper.term for paper in question_papers)
        term_data = list(term_data)
        seatingDetails = []
        total_student_count = 0
        total_department_count = 0
        for seating in seating_arrangements:
            seatingDetails.append({
               'hall_name' : seating.hall_name ,
               'department_students' : seating.department_students,
               'term_data'           : term_data,
               'teacher'             : seating.teacher.name
            })
        #     student_count = sum(len(student_list) for student_list in department_students.values())
        #     total_student_count += student_count
        #     department_count = len(department_students)
        #     total_department_count += department_count
        #     department_id = list(department_students.keys())[0]
        #     if department_students:
        #         department_id = list(department_students.keys())[0]
        #         department = Department.objects.get(id=department_id)
        #         department_code = department.department_code
        #     else:
        #         department_code = 'N/A'
        #     department_student_counts = {}
        #     for seating in seating_arrangements:
        #         try:
        #             department_students = json.loads(seating.department_students)
        #         except json.JSONDecodeError:
        #             department_students = []
        #         department_codes = set()
                # for row in department_students:
                #     for group in row:
                #         for seat in group:
                #             if seat != "Vacant-0":
                #                 department_code, _ = seat.split("-")[0]
                #                 department_codes.add(department_code)
                #                 if department_code not in department_student_counts:
                #                     department_student_counts[department_code] = 1
                #                 else:
                #                     department_student_counts[department_code] += 1
            # total_departments = len(department_student_counts)
            # total_student_count = sum(department_student_counts.values())
            # detail = {
            #     'hall_name': seating.hall_name,
            #     'teacher': seating.teacher.name,
            #     'term_data': term_data,
            #     'total_departments': total_departments,
            #      'total_students': total_student_count,
            #     'department_students' : seating.department_students,
                #  'department_code'     : department_code
            #     'department_details': [
            #     {'department_code': dept_code, 'student_count': count}
            #     for dept_code, count in department_student_counts.items()
            # ]
            # }
            # print(detail , "detaillllllllllll")
            # seatingDetails.append(detail)
        return JsonResponse(seatingDetails, safe=False)
        

        

        
    

        
        
        