from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from app1.models import *
from app1.serializers import *
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import *
from .serializers import *
import base64
import json
from django.db import transaction


#Student Login
class StudentLogin(APIView):

    def post(self , request , *args , **kwargs):
        roll_no  = request.data.get('roll_no')
        password = request.data.get('password')


        try:
            user = Student.objects.get(roll_no = roll_no , password = password)

            print(user,"..user")

        except Student.DoesNotExist:
            user = None
        # if user is not None and check_password(password,user.password):
        #     return JsonResponse({'message': 'Login successful'})
        
        if user is not None :
            print("enterrrrrrrrrrrrrrr")
            return JsonResponse({'message': 'Login successful'})
        
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)



class Scribble(APIView):
    def post(self, request, *args, **kwargs):
        
        try:
            data = request.data
            image_name = data.get('image_name')
            data_values = data.get('data')
            byte_instance = Byte.objects.create(image_name=image_name, datas=data_values)
            return JsonResponse({'message': 'Byte instance created successfully.'})

        except Exception as e:
            print(e , 'entereeeeeeed')
            return JsonResponse({'error': str(e)}, status=400)

  
    def get(self, request, *args, **kwargs):
      
    
        bytes = Byte.objects.all()

        bytesDetails = []

        for byte in bytes:
            bytesDetails.append({

            
                'image_name':byte.image_name,
                'data':byte.datas,
            })
        print(bytesDetails)

        return JsonResponse(bytesDetails, safe=False)


        

           
        
    




    

