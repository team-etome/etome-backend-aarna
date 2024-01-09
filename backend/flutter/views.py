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
    
    def post(self, request):
        image_name = request.data.get('image_name')
        byte_data = request.data.get('data')

        if byte_data is not None:
            byte_data = base64.b64decode(byte_data)
            byte_instance = Byte(image_name=image_name, data=byte_data)
            byte_instance.save()

            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'message': 'No data provided'}, status=400)

    def get(self, request):
        byte_objects = Byte.objects.all()

        data_list = []
        for byte_object in byte_objects:
            encoded_data = base64.b64encode(byte_object.data).decode('utf-8')
            data_list.append({
                'image_name': byte_object.image_name,
                'data': encoded_data
            })
            
        return JsonResponse(data_list, safe=False)




    

