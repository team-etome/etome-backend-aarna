from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import * 
from rest_framework.exceptions import ValidationError
from . token import get_token
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import login




class AdminLoginView(APIView):

    def post(self, request, *args, **kwargs):
        email     =  request.data.get('email')
        password  =  request.data.get('password')


        try:
            user = God.objects.get(email = email)
        except God.DoesNotExist:
            user = None

        if user is not None and check_password(password , user.password) and user.is_superuser:
            login(request , user)


            admin_token = get_token(user , user_type='admin')


            return JsonResponse({'message': 'Login successful','token' : admin_token })
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        

        





