from rest_framework import status
from rest_framework.views import APIView
from .models import *
from .serializers import * 
from . token import get_token
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from rest_framework.response import Response



class GodLoginView(APIView):
    

    def post(self, request, *args, **kwargs):
        try:
            email     =  request.data.get('email')
            password  =  request.data.get('password')

            if not email or not password:
             return JsonResponse({'error': 'Email and password are required'}, status=400)

            try:
                user = God.objects.get(email = email)
            except God.DoesNotExist:
                return JsonResponse({'error': 'No user found with this email'}, status=404)
            except Exception as e:
             return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)


            if check_password(password, user.password):


                admin_token = get_token(user , user_type='god')
                return JsonResponse({'message': 'Login successful','token' : admin_token })
            
            else:

                return JsonResponse({'error': 'Invalid email or password'}, status=401)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




class AdminLoginView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('emailid')
        password = request.data.get('password')

        if not email or not password:
            return JsonResponse({'error': 'Email and password are required'}, status=400)

        try:
            user = Admin.objects.get(emailid=email)
        except Admin.DoesNotExist:
            return JsonResponse({'error': 'No admin found with this email'}, status=404)
        except Exception as e:
            return JsonResponse({'error': 'An unexpected error occurred: ' + str(e)}, status=500)

        if check_password(password, user.password):
            admin_token = get_token(user, user_type='admin')
            return JsonResponse({'message': 'Login successful', 'token': admin_token})
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=401)


class AddAdmin(APIView):
    def post(self, request):
        try:
            data = request.data

            admin_serializer = AdminSerializer(data=data)

            if admin_serializer.is_valid():
                admin_serializer.save()
                return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(admin_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

        except Exception as e:
            return JsonResponse({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        

class AddDepartment(APIView):
    def post(self, request):
        try:
            data = request.data
            print(data , "dataaaaaaaaaaa")
            name = data.get('department')
            code = data.get('department_code')

            if Department.objects.filter(department=name).exists():
                return JsonResponse({'error': 'A department with this name already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if Department.objects.filter(department_code=code).exists():
                return JsonResponse({'error': 'A department with this code already exists.'}, status=status.HTTP_400_BAD_REQUEST)

            department_Serializer = DepartmentSerializer(data=data)
            if department_Serializer.is_valid():
                department_Serializer.save()
                return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
            else:
                print(department_Serializer.errors ,"errorssssssssssssssss")
                return JsonResponse(department_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        try:
            departments = Department.objects.all().order_by('id')
            departmentDetails = []

            for department in departments:
                departmentDetails.append({
                    'id': department.id,
                    'departmentName': department.department,
                    'departmentCode': department.department_code,
                    'program': department.program,
                    'total_sem': department.total_sem
                })
            return JsonResponse(departmentDetails, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request,pk):
            data = request.data

            print(data ,"dataaaaaaaaaaaaaaa")
            id = data.get('id')
            department = Department.objects.get(id=id)
        
            if 'department' in data:
                department.department = data['department']
            if 'department_code' in data:
                department.department_code = data['department_code']
            if 'program' in data:
                department.program = data['program']
            if 'total_sem' in data:
                department.total_sem = data['total_sem']
            department.save()
            return JsonResponse({"message": "Department updated successfully"}, status=status.HTTP_200_OK)
       


    def delete(self, request, pk):
        try:
            department = Department.objects.get(id=pk)
            department.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)





class AddSubject(APIView):
    def post(self,request):
        data = request.data
        name = data.get('subject')
        code = data.get('subject_code')
        department=data.get('department')

        if Subject.objects.filter(subject=name, department=department).exists():
            return JsonResponse({'error':'a subject with same name already exists'},status=status.HTTP_400_BAD_REQUEST)
        if Subject.objects.filter(subject_code=code, department=department).exists():
            return JsonResponse({'error':'a subject with the code already exists'},status=status.HTTP_400_BAD_REQUEST)       
        subject_Serializer = SubjectSerializer(data = data)
        if subject_Serializer.is_valid():
            subject_Serializer.save()

            return JsonResponse({'message': 'Data saved successfully'}, status=status.HTTP_201_CREATED)
        
        else:
            return JsonResponse(subject_Serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            

    def get(self,request):
        try:
      
            subjects = Subject.objects.all().order_by('id')
        
            subjectDetails = []

            for subject in subjects:
            
                subjectDetails.append({

                    'id'       : subject.id,
                    'subjectName' : subject.subject,
                    'subjectCode'   : subject.subject_code,
                    'programme'   : subject.programme,
                    'semester'    : subject.semester , 
                    'department_id' : subject.department_id,
                    'department_name'  : subject.department.department,
                    'elective'         : subject.elective
                    
                })


            return JsonResponse(subjectDetails, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def put(self , request):

        data = request.data
        id   = data.get('id')

        try:
            subject = Subject.objects.get(id = id)

        except Subject.DoesNotExist:
            return JsonResponse({"messaage" : "Subject not found"},status=404)
        
        if 'subject' in data:
            subject.subject = data['subject']
        if 'subject_code' in data:
            subject.subject_code = data['subject_code']
        if 'programme' in data:
            subject.programme = data['programme']

        if 'semester' in data:
            subject.semester = data['semester']

        subject.save()
        return JsonResponse({"message": "Subject updated successfully"}, status=200)

    def delete(self, request, pk):
        try:
            subject = Subject.objects.get(id=pk)
            subject.delete()
            return JsonResponse(status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return JsonResponse(status=status.HTTP_404_NOT_FOUND)




class SendInvite(APIView):

    def post(self,request):

        email_addresses = request.data.get('emails', [])
        if not email_addresses:
            return JsonResponse({"error": "No email addresses provided."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            for email in email_addresses:
                self.send_mail(email)
            return JsonResponse({"message": "Emails sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



    def send_mail(self, recipient_email):
        sender_mail = "development@resoluteindia.co.in"
        password = "csjpwswsxucprkxb"
        subject = "Invitation to Join Our Exciting Platform!"

        html = """
            <html>
                 <head>
        <style>
            .email-card {
                font-family: 'Arial', sans-serif;
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                border: 1px solid #ddd;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                border-radius: 8px;
                text-align: center;
            }
            .email-card img {
                width: 200px;
                height: auto;
                margin-bottom: 20px;
            }
            .email-card a {
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                border-radius: 8px;
                margin-top: 20px;
                margin-bottom: 20px; /* Adjusted space after button */
            }
            .email-card p {
                color: #333;
                line-height: 1.5;
                margin-bottom: 10px; /* Reduced bottom margin for paragraphs */
            }
            .email-card p:last-child {
                margin-bottom: 0; /* Removes bottom margin from the last paragraph */
            }
        </style>
    </head>
    <body>
        <div class="email-card">
            <h1>Welcome to Etome  </h1>
            <img src="cid:etome_logo" alt="Etome Logo">
            <p>In collaboration with [School Name]</p>
            <p>We're thrilled to have you join our community of dedicated educators. As a member, you'll have access to exclusive resources, networking opportunities, and the latest insights in education.</p>
            <a href="http://localhost:5173/tregister">Join Now</a>
            <p>If you have any questions, feel free to contact us at any time.</p>
            <p>Best Regards,<br>Team Etome</p>
        </div>
    </body>
        </html>
        """

        msg = MIMEMultipart('alternative')
        msg['From'] = sender_mail
        msg['To'] = recipient_email
        msg['Subject'] = subject

       
        msg.attach(MIMEText(html, 'html'))

        with open('static\Etomeogo2.png ', 'rb') as f:
            logo = MIMEImage(f.read())
            logo.add_header('Content-ID', '<etome_logo>')
            msg.attach(logo)

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_mail, password)
            server.sendmail(sender_mail, recipient_email, msg.as_string())
            server.quit()
        except Exception as e:
            return JsonResponse(f"Error sending email: {str(e)}",status=status.HTTP_400_BAD_REQUEST)
      


    


class AddTeacher(APIView):
    def post(self, request):
            data = request.data.copy()
            department_ids = data.get('department_id')
            subject_ids = data.get('subject_id')
            phone=data.get('phoneNumber')
            email=data.get('email')
            if Teacher.objects.filter(phoneNumber=phone).exists():
                return JsonResponse({'error': ' Phone number already exists.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if Teacher.objects.filter(email=email).exists():
                return JsonResponse({'error': 'email already exists.'}, status=status.HTTP_400_BAD_REQUEST) 

            
            if department_ids:
                if isinstance(department_ids, str) and ',' in department_ids:
                    department_ids = [int(id.strip()) for id in department_ids.split(',')]
                else:
                    department_ids = [int(department_ids)]
                data.setlist('departments', department_ids)

            if subject_ids:
                if isinstance(subject_ids, str) and ',' in subject_ids:
                    subject_ids = [int(id.strip()) for id in subject_ids.split(',')]
                else:
                    subject_ids = [int(subject_ids)]
                data.setlist('subjects', subject_ids)

            teacher_serializer = TeacherSerializer(data=data)
            if teacher_serializer.is_valid():
                teacher = teacher_serializer.save()
                image_url = teacher.image.url

                return JsonResponse({'message': 'Teacher added successfully'}, status=status.HTTP_201_CREATED)
            else:
                subject_ids = [int(subject_ids)]
            data.setlist('subjects', subject_ids)

            teacher_serializer = TeacherSerializer(data=data)
            if teacher_serializer.is_valid():
                teacher = teacher_serializer.save()
                image_url = teacher.image.url

                return JsonResponse({'message': 'Teacher added successfully'}, status=status.HTTP_201_CREATED)
            else:
                return JsonResponse(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

        

        



