from .views import *
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [ 

     path ('api/adminLogin',views.AdminLoginView.as_view(),name='adminlogin'),
     path ('api/godLogin',views.GodLoginView.as_view(),name='godlogin'),
     path ('api/addadmin',views.AddAdmin.as_view() , name='addadmin'),
     path('api/addDepartment',views.AddDepartment.as_view(),name='addDepartment'),
     path('api/addSubject',views.AddSubject.as_view(),name='addSubject'),
     path('api/addDepartment/<int:pk>', views.AddDepartment.as_view(), name='delete_department'),

  

]






