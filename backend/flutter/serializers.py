# from rest_framework import serializers
# from flutter.models import *



# class DataSerializer(serializers.ModelSerializer):


    class Meta:
        model = Byte
        fields = ['image_name','data']

    