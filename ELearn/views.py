from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from ELearn.models import Course, Module, Topic, Assessment, Question, Assessment_Attempt
from django.http import HttpResponse
from ELearn.forms import CreateModuleForm, CreateTopicForm, CreateAssessmentForm, CreateQuestions
from django.template import RequestContext
from django.urls import reverse

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
		create_module_form.instance.module_type = 'CW'
		module = create_module_form.save()
		messages.success(request, f'✔️ Module created')
		return redirect('createtopic',module_id=module.module_id)

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
	module = Module.objects.get(module_id=module_id)
	module_name = module.module_name
	course = Course.objects.get(course_id=module.course.course_id)

	if request.method == 'POST':
		create_topic_form = CreateTopicForm(request.POST, request.FILES)
		create_topic_form.instance.module = Module.objects.get(module_id=module_id)
		create_topic_form.save()
		messages.success(request, f'✔️ Topic created')
		return redirect('coursehome', course_id=course.course_id)	

	return render(request, "ELearn/create_topic.html", {"form" : create_topic_form, "module_id":module_id, "module_name":module_name})

def open_document(request, course_id, module_id, file_path):
	
	file_path = f"http://127.0.0.1:8000/media/{course_id}/{module_id}/{file_path}"
	return render(request, "ELearn/open_document.html", {"file_path" : file_path})


def create_assessment(request, course_id):

	create_assess_form = CreateAssessmentForm()
	course = Course.objects.get(course_id=course_id)

	if request.method == 'POST':
		create_assess_form = CreateAssessmentForm(request.POST)
		assessment = create_assess_form.save(False)
		module = Module(module_name = assessment.assess_name, module_type = 'AS', course=course)
		module.save()
		create_assess_form.instance.module = module.module_id
		create_assess_form.instance.course = course
		assessment = create_assess_form.save()
		messages.success(request, f'✔️ Assessment created')
		return redirect('addquestions', assess_id=assessment.assess_id)	

	return render(request, "ELearn/create_assessment.html", {"form" : create_assess_form, "course_id":course_id})

def add_questions(request, assess_id):

	add_question_form = CreateQuestions()

	if request.method == 'POST':
		add_question_form = CreateQuestions(request.POST)
		add_question_form.instance.assessment = Assessment.objects.get(assess_id = assess_id)		
		add_question_form.save()
		messages.success(request, f'✔️ Question added')
		add_question_form = CreateQuestions()
		return render(request, "ELearn/add_questions.html", {"form" : add_question_form, "assess_id":assess_id})	
	return render(request, "ELearn/add_questions.html", {"form" : add_question_form, "assess_id":assess_id})

def module_home(request, module_id):

	module = Module.objects.get(module_id=module_id)
	return render(request, "ELearn/module_home.html", {"module":module})

def assessment_home(request, module_id):

	assessment = Assessment.objects.get(module=module_id)
	questions = Question.objects.filter(assessment=assessment.assess_id)
	is_published = assessment.is_published
	return render(request, "ELearn/assessment_home.html", {"questions":questions, "module_id":module_id, "is_published":is_published})

def take_assessment(request, module_id):	

	assessment = Assessment.objects.get(module=module_id)
	questions = Question.objects.filter(assessment=assessment.assess_id)

	if request.method == 'POST':
		
		for question in questions:
			result = 0
			field_id = f'{question.question_id}_answer'	
			answer = request.POST.get(field_id)	
			correct_answer = question.answer_text
			if (answer.lower() == correct_answer.lower()):
				result = question.question_points		
			assess_attempt = Assessment_Attempt(attempt_user=request.user,assessment = assessment, 
								question = question, answer = answer, result=result)
			assess_attempt.save()

		messages.success(request, f'✔️ Attempt saved!')
		course_list = Course.objects.filter(instructor=request.user)
		return render(request, "ELearn/home.html", {"Courses": course_list})

	return render(request, "ELearn/take_assessment.html", {"questions":questions, "assessment":assessment})

def publish_assessment(request, module_id):
	assessment = Assessment.objects.get(module=module_id)
	assessment.is_published = True
	assessment.save()
	messages.success(request, f'✔️ Assessment published')
	questions = Question.objects.filter(assessment=assessment.assess_id)
	return render(request, "ELearn/assessment_home.html", {"questions":questions, "module_id":module_id, "is_published":assessment.is_published})