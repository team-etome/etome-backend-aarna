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
from .serializers import *






#Login of God(super user)
class GodLoginView(APIView):

    def post(self, request, *args, **kwargs):
        email     =  request.data.get('email')
        password  =  request.data.get('password')


        try:
            user = God.objects.get(email = email)
        except God.DoesNotExist:
            user = None

        if user is not None and check_password(password , user.password):
            login(request , user)

            admin_token = get_token(user , user_type='admin')


            return JsonResponse({'message': 'Login successful','token' : admin_token })
        
        else:

            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        


#Login of Admin(college)
class AdminLoginView(APIView):

    def post(self, request, *args, **kwargs):
        email     =  request.data.get('emailid')
        password  =  request.data.get('password')

        print(email , password ,".............")

        try:
            user = Admin.objects.get(emailid = email)
            print(user,"userrrrrrrrrrrr")
        except Admin.DoesNotExist:
            user = None

        if user is not None and check_password(password , user.password):
            # login(request , user)

            admin_token = get_token(user , user_type='admin')


            return JsonResponse({'message': 'Login successful','token' : admin_token })
        
        else:

            return JsonResponse({'error': 'Invalid credentials'}, status=401)
        




#adding colleges(admin) by God
class AddAdmin(APIView):
    def post(self , request):
        data = request.data
        admin_serializer = AdminSerializer(data=data)
       
        if admin_serializer.is_valid():
            admin_serializer.save()

            return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

        

        





