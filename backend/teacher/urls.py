from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from teacher import views



urlpatterns = [ 

     path('api/teacher', views.TeacherDetails.as_view(), name='teacher'),

   

]