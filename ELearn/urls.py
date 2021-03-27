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
    path('editmodule/<str:module_id>', views.edit_module, name="editmodule"),
    path('deletemodule/<str:module_id>', views.delete_module, name='deletemodule'),
    path("modulehome/<str:module_id>", views.module_home, name="modulehome"), 
    path("coursehome/<str:course_id>", views.course_home, name='coursehome'), 
    path("coursedetail/<str:course_id>", views.course_detail , name='coursedetail'),
    path("createtopic/<str:module_id>", views.create_topic , name='createtopic'),
    path("deletetopic/<int:topic_id>", views.delete_topic , name='deletetopic'),
    path("opendocument/<str:course_id>/<str:module_id>/<str:file_path>", views.open_document, name="opendocument"),
    path("createassessment/<str:course_id>", views.create_assessment , name='createassessment'),
    path("addquestions/<str:assess_id>", views.add_questions , name='addquestions'),
    path("deletequestion/<int:ques_id>", views.delete_question , name='deletequestion'),
    path("assessmenthome/<str:module_id>", views.assessment_home, name="assessmenthome"),
    path("takeassessment/<str:module_id>", views.take_assessment, name="takeassessment"),
    path("publishassessment/<str:module_id>", views.publish_assessment, name="publishassessment"),
    path("studentstats/<str:module_id>", views.view_student_stats, name="studentstats"),
    path("uploadquestions/<str:assess_id>", views.upload_questions , name='uploadquestions'),
    path("composemessage/", views.compose_message , name='composemessage'),
    path("inbox/", views.inbox , name='inbox'),
    path("sentitems/", views.sent_items , name='sentitems'),
    path("creatediscussion/", views.create_discussion , name='creatediscussion'),
    path("postcomment/<str:topic>", views.post_comment , name='postcomment'),
    path("discussions/", views.view_discussion , name='discussions'),
    path("createassignment/<str:course_id>", views.create_assignment , name='createassignment'),
    path("createproject/<str:course_id>", views.create_project , name='createproject'),
    path("assignmenthome/<str:module_id>", views.assignment_home , name='assignmenthome'),
    path("projecthome/<str:module_id>", views.project_home , name='projecthome'),
]
