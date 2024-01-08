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
            })

        return JsonResponse(teacherDetails, safe=False)


