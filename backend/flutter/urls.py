from .views import * 
from django.urls import path
from flutter import views 
from django.conf.urls.static import static



urlpatterns = [


    path('api/studentLogin',views.StudentLogin.as_view() , name='studentLogin'),
    path('api/addstudent',views.AddStudent.as_view() , name='addstudent'),
    path('api/submitAnswer',views.Answers.as_view() , name='submitAnswer'),
    
    # path('api/scribble',views.Scribble.as_view() , name='scribble'),




]