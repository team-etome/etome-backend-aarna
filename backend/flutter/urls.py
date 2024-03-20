from .views import * 
from django.urls import path
from flutter import views 
from django.conf.urls.static import static



urlpatterns = [
    path('api/studentExaminationLogin',views.StudentExaminationLogin.as_view() , name='studentExaminationLogin'),
    path('api/addStudent',views.AddStudent.as_view() , name='addStudent'),
    path('api/submitAnswer',views.Answers.as_view() , name='submitAnswer'),
    path('api/evaluation',views.Evaluations.as_view() , name='evaluation'),
    path('api/EvaluationLogin',views.EvaluationLogin.as_view() , name='EvaluationLogin'),
    path('api/uploadExcel',views.UploadExcelStudent.as_view() , name='UploadExcelStudent'),
    
]