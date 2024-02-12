from django.contrib import admin
from .models import *
from aarna.models import *
from flutter.models import *


# app1
admin.site.register(God)
admin.site.register(Department)
admin.site.register(Semester)
admin.site.register(Subject)
admin.site.register(Student)
admin.site.register(Admin)
admin.site.register(Teacher)
admin.site.register(QuestionPaper)


#flutter
admin.site.register(Questions)
admin.site.register(QuestionImage)
admin.site.register(AnswerImage)
admin.site.register(Answer)
admin.site.register(AssignEvaluation)
admin.site.register(Evaluation)
admin.site.register(SeatingArrangement)


#aarna
admin.site.register(TimeTable)

