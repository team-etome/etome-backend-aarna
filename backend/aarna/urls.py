from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from aarna import views


urlpatterns = [ 

    path('api/timetable', views.TimeTable.as_view(), name='timetable'),


    




]