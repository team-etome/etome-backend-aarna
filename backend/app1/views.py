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
# from django.shortcuts import get_object_or_404


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

     

        try:
            user = Admin.objects.get(emailid = email)
         
        except Admin.DoesNotExist:
            user = None

        if user is not None and check_password(password , user.password):

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
        departments = Department.objects.all().order_by('id')
        print(departments , "departmentss")
        departmentDetails = []

        for department in departments:
            departmentDetails.append({

                'id'           :  department.id,
                'departmentName': department.department,
                'departmentCode': department.department_code,
                'department_head': department.department_head,
            })

        return JsonResponse(departmentDetails, safe=False)
    

    def put(self , request):
        data = request.data
        id = data.get('id')
        try:
            department = Department.objects.get(id=id)
        except Department.DoesNotExist:
            return Response({"message": "Department not found"}, status=404)

        if 'department' in data:
            department.department = data['department']
        if 'department_code' in data:
            department.department_code = data['department_code']
        if 'department_head' in data:
            department.department_head = data['department_head']

        department.save()

        return Response({"message": "Department updated successfully"}, status=200)
    

    def delete(self, request, pk):
        try:
            department = Department.objects.get(id=pk)
            department.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)




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
            

    def get(self,request):
      
        subjects = Subject.objects.all().order_by('id')
        print(subjects)


        subjectDetails = []

        for subject in subjects:
          
            subjectDetails.append({

                'id'       : subject.id,
                'subjectName' : subject.subject,
                'subjectCode'   : subject.subject_code,
                'programme'   : subject.programme

            })


        return JsonResponse(subjectDetails, safe=False)


    def put(self , request):

        data = request.data
        id   = data.get('id')

      

        try:
            subject = Subject.objects.get(id = id)

        except Subject.DoesNotExist:
            return Response({"messaage" : "Subject not found"},status=404)
        

        if 'subject' in data:
            subject.subject = data['subject']
        if 'subject_code' in data:
            subject.subject_code = data['subject_code']
        if 'programme' in data:
            subject.programme = data['programme']

        subject.save()

        return Response({"message": "Subject updated successfully"}, status=200)


    def delete(self, request, pk):
        print("enterrrrrrrrrr")
        try:
            subject = Subject.objects.get(id=pk)
            subject.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)





     
           

       
        

        

        





