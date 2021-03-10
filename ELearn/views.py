from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from ELearn.models import Course
from django.http import HttpResponse
from ELearn.forms import CreateModuleForm
from django.template import RequestContext
from django.urls import reverse

# Create your views here.
def home(request):
	course_list = []	
	if request.user.is_authenticated:		
		current_user = request.user
		course_list = Course.objects.filter(instructor=current_user)
	return render(request, "ELearn/home.html", {"Courses": course_list})
	
def create_modules(request, course_id):	
	create_module_form = CreateModuleForm()
	if request.method == 'POST':
		create_module_form = CreateModuleForm(request.POST)
		create_module_form.instance.course = Course.objects.get(course_id=course_id)
		create_module_form.save()
		messages.success(request, f'✔️ Module created')
		return redirect('home')	
	return render(request, "ELearn/createmodule.html", {"form" : create_module_form, "course_id":course_id})

def course_details(request, course_id):	
	course = Course.objects.get(course_id=course_id)
	return render(request, "ELearn/course_detail.html", {"course": course})
	