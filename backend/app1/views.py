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
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage



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
        try:
            subject = Subject.objects.get(id=pk)
            subject.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Department.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class SendInvite(APIView):

    def post(self,request):
        
        email_addresses = request.data.get('emails', [])

        if not email_addresses:
            return Response({"error": "No email addresses provided."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            for email in email_addresses:
                self.send_mail(email)
            return Response({"message": "Emails sent successfully."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
            print("Email sent successfully to", recipient_email)
        except Exception as e:
            print("Error sending email:", str(e))

    


#Add Teacher   
class AddTeacher(APIView):
    def post(self, request):
        data = request.data.copy()
        department_ids = data.get('department_id')
        subject_ids = data.get('subject_id')

        
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
            teacher_serializer.save()
            return Response({'message': 'Teacher added successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response(teacher_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        

        

        





