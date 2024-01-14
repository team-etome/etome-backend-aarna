from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from teacher import views



urlpatterns = [ 

     path('api/teacher', views.TeacherDetails.as_view(), name='teacher'),
     path('api/deleteTeacher/<int:pk>', views.TeacherDetails.as_view(), name='delete_teacher'),
     path('api/assign_blueprint/', views.AssignBlueprint.as_view(), name='assign_blueprint_api'),
     path('api/blueprint/<int:pk>/', views.BlueprintDetailAPI.as_view(), name='blueprint_detail_api'),
     path('api/blueprint_review/<int:pk>/', views.BlueprintReviewAPI.as_view(), name='blueprint_review_api'),
     path('api/teacherlogin', views.TeacherLoginView.as_view(), name='teacherlogin'),

   

]