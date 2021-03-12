from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from ELearn.models import Course, Module, Topic
from django.http import HttpResponse
from ELearn.forms import CreateModuleForm, CreateTopicForm
from django.template import RequestContext
from django.urls import reverse

# Create your views here.

def home(request):
	course_list = []	
	if request.user.is_authenticated:		
		current_user = request.user
		course_list = Course.objects.filter(instructor=current_user)
	return render(request, "ELearn/home.html", {"Courses": course_list})
	
def create_module(request, course_id):	
	create_module_form = CreateModuleForm()
	if request.method == 'POST':
		create_module_form = CreateModuleForm(request.POST)
		create_module_form.instance.course = Course.objects.get(course_id=course_id)
		create_module_form.save()
		messages.success(request, f'✔️ Module created')
		return redirect('home')	
	return render(request, "ELearn/create_module.html", {"form" : create_module_form, "course_id":course_id})

def course_home(request, course_id):	
	course = Course.objects.get(course_id=course_id)
	modules = Module.objects.filter(course=course)
	topics = Topic.objects.filter(module__in=modules)
	return render(request, "ELearn/course_home.html", {"course": course, "modules":modules, "topics":topics})

def course_detail(request, course_id):	
	course = Course.objects.get(course_id=course_id)
	return render(request, "ELearn/course_detail.html", {"course": course})

def create_topic(request, module_id):	
	create_topic_form = CreateTopicForm()
	if request.method == 'POST':
		create_topic_form = CreateTopicForm(request.POST, request.FILES)
		create_topic_form.instance.module = Module.objects.get(module_id=module_id)
		create_topic_form.save()
		messages.success(request, f'✔️ Topic created')
		return redirect('home')	
	return render(request, "ELearn/create_topic.html", {"form" : create_topic_form, "module_id":module_id})

def open_document(request, course_id, module_id, file_path):
	file_path = "http://127.0.0.1:8000/media/"+course_id+"/"+module_id+"/"+file_path
	# http://127.0.0.1:8000/media/course_CSIT-598/1/Requirements.docx
	# <!-- http://127.0.0.1:8000/opendocument/course_CSIT-598/1/Requirements.docx -->
	return render(request, "ELearn/open_document.html", {"file_path" : file_path})