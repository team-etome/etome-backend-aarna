from django.contrib import admin
from django.urls import path,include
from app1 import views


urlpatterns = [
    path('admin/', admin.site.urls),


    # path('', include('app1.urls')),


    path ('api/adminLogin',views.AdminLoginView.as_view(),name='adminlogin')






    
]
