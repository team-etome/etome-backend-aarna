from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from app1.models import *
from flutter.models import *
from app1.serializers import * 
from flutter.serializers import * 
from rest_framework.exceptions import ValidationError
from app1.token import get_token
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from django.conf import settings




class TimeTable(APIView):

    def get(self , request):
        questionpapers = QuestionPaper.objects.all().order_by('exam_date')


        for questionpaper in questionpapers:
            TimeTable.objects.create(
                exam_name=questionpaper.exam_name,
                department=questionpaper.department,
                subject=questionpaper.subject,
                exam_date=questionpaper.exam_date,
                exam_time=questionpaper.total_time,
            )

       

        

        

        