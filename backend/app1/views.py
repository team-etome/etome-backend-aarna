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
from django.shortcuts import get_object_or_404


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

            admin_token = get_token(user , user_type='god')


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


#Add Department    
class AddDepartment(APIView):
    def post(self,request):

        data = request.data
        department_Serializer = DepartmentSerializer(data = data)

        if department_Serializer.is_valid():
            department_Serializer.save()

            return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        
        else:
            return Response(department_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def get(self, request):
        print("Entering GET request")

        departments = Department.objects.all()

        departmentDetails = []

        for department in departments:
            departmentDetails.append({

                'id'           :  department.id,
                'departmentName': department.department,
                'departmentCode': department.department_code,
                'department_head': department.department_head,
            })

        # print(departmentDetails)
    
        return JsonResponse(departmentDetails, safe=False)
            



#Add subject
class AddSubject(APIView):
    def post(self,request):

        data = request.data
        subject_Serializer = SubjectSerializer(data = data)

        if subject_Serializer.is_valid():
            subject_Serializer.save()

            return Response({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        
        else:
            return Response(subject_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            





     
           

       
        

        

        





