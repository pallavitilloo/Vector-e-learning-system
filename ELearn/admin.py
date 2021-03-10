from django.contrib import admin
from .models import Profile, Course, Module, Topic, Assessment, Question, Assessment_Attempt, Assignment, Submission

# Register your models here.
admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Assessment)
admin.site.register(Question)
admin.site.register(Topic)
admin.site.register(Assessment_Attempt)
admin.site.register(Assignment)
admin.site.register(Submission)