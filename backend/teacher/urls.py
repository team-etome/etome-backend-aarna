from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from teacher import views



urlpatterns = [ 

     path('api/teacher', views.TeacherDetails.as_view(), name='teacher'),
     path('api/deleteTeacher/<int:pk>', views.TeacherDetails.as_view(), name='delete_teacher'),
     path('api/assignBlueprint', views.AssignBlueprint.as_view(), name='assign_blueprint_api'),
     path('api/teacherlogin', views.TeacherLoginView.as_view(), name='teacherlogin'),
     path('api/getBlueprintDetails/<int:id>', views.BlueprintDetailView.as_view(), name='get_blueprint_details'),
     path('api/qpapermodule', views.QpaperModule.as_view(), name='qpapermodule'),
     path('api/qpapermodule/<int:qpaperid>', views.QpaperModule.as_view(), name='qpapermodule'),
     path('api/seatingArrangement', views.SeatingArrangementView.as_view(), name='seatingA rrangement'),
      


   

]