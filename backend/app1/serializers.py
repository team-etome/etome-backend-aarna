from rest_framework import serializers
from app1.models import *
from django.contrib.auth.hashers import make_password



class GodSerializer(serializers.ModelSerializer):

    class Meta:
        model = God
        field = ['email','password']
