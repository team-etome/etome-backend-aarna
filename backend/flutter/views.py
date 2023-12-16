from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from app1.models import *
from app1.serializers import *
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse




#Student Login
class StudentLogin(APIView):

    def post(self , request , *args , **kwargs):
        roll_no  = request.data.get('roll_no')
        password = request.data.get('password')

        try:
            user = Student.objects.get(roll_no = roll_no)

        except Student.DoesNotExist:
            user = None

        
        if user is not None and check_password(password,user.password):
            return JsonResponse({'message': 'Login successful'})
        
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

