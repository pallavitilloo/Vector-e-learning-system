from django.urls import path
from ELearn import views
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.http import request
admin.autodiscover()

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", auth_views.LoginView.as_view(template_name='ELearn/login.html'), name="login"),
    path("logout/", auth_views.LogoutView.as_view(template_name='ELearn/logout.html'), name="logout"),
    path("createmodule/<str:course_id>", views.create_module, name="createmodule"),  
    path("modulehome/<str:module_id>", views.module_home, name="modulehome"), 
    path("coursehome/<str:course_id>", views.course_home, name='coursehome'), 
    path("coursedetail/<str:course_id>", views.course_detail , name='coursedetail'),
    path("createtopic/<str:module_id>", views.create_topic , name='createtopic'),
    path("opendocument/<str:course_id>/<str:module_id>/<str:file_path>", views.open_document, name="opendocument"),
    path("createassessment/<str:course_id>", views.create_assessment , name='createassessment'),
    path("addquestions/<str:assess_id>", views.add_questions , name='addquestions'),
    path("assessmenthome/<str:module_id>", views.assessment_home, name="assessmenthome"),
    path("takeassessment/<str:module_id>", views.take_assessment, name="takeassessment"),
    path("publishassessment/<str:module_id>", views.publish_assessment, name="publishassessment"),
    path("studentstats/<str:module_id>", views.view_student_stats, name="studentstats"),
    path("uploadquestions/<str:assess_id>", views.upload_questions , name='uploadquestions'),
    path("composemessage/", views.compose_message , name='composemessage'),
    path("inbox/", views.inbox , name='inbox'),
    path("sentitems/", views.sent_items , name='sentitems'),
]
