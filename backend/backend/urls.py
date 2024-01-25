from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static




urlpatterns = [
    path('admin/', admin.site.urls),


    path('', include('app1.urls')),

    path('', include('flutter.urls')),

    path('', include('teacher.urls')),

    path('', include('aarna.urls')),


   
    
] + static (settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
