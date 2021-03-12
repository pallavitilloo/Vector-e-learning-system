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
    path("createmodule/<str:course_id>", views.create_module),   
    path("coursehome/<str:course_id>", views.course_home), 
    path("coursedetail/<str:course_id>", views.course_detail),
    path("createtopic/<str:module_id>", views.create_topic),
    path("opendocument/<str:course_id>/<str:module_id>/<str:file_path>", views.open_document),
]
