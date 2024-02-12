from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from aarna import views


urlpatterns = [ 

    path('api/timetable', views.Timetable.as_view(), name='timetable'),
    path('api/hallticket', views.HallTicket.as_view(), name='hallticket'),
    path('api/evaluationAssign',views.EvaluationAssign.as_view(),name='evaluationAssign'),
    path('api/Questions',views.QuestionsView.as_view(),name='Questions'),
    path('api/invigilatorLogin',views.InvgilatorLogin.as_view(),name='invigilator'),


]