from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from ELearn.models import Course, Module, Topic, Assessment, Question, Assessment_Attempt, Message, User, Comment, Assignment, Project
from django.http import HttpResponse, request
from ELearn.forms import CreateModuleForm, CreateTopicForm, CreateAssessmentForm, CreateQuestions, CreateMessage, CreateDiscussion, PostComment, CreateAssignment, CreateProject
from django.template import RequestContext
from django.urls import reverse
from django.db.models import Sum
from pyexcel_xlsx import get_data as xlsx_get
from django.utils.datastructures import MultiValueDictKeyError

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

def edit_module(request, module_id):	
    
	module = Module.objects.get(module_id = module_id)
	create_module_form = CreateModuleForm(request.POST or None, instance = module)
	
	if create_module_form.is_valid():
		create_module_form.save()
		return render(request, "ELearn/module_home.html", {"module":module})
	
	return render(request, "ELearn/create_module.html", {"form" : create_module_form, "course_id":module.course.course_id})	

def delete_module(request, module_id):	
    
	module = Module.objects.get(module_id = module_id)	
	course = Course.objects.get(course_id = module.course.course_id)	
	if module.module_type == 'AS':
		assessment = Assessment.objects.get(module = module_id)
		assessment.delete()
	elif module.module_type == 'AT':
		assignment = Assignment.objects.get(module=module_id)
		assignment.delete()
	elif module.module_type == 'PT':
		project = Project.objects.get(module = module_id)
		project.delete()

	module.delete()
	
	modules = Module.objects.filter(course=course)
	topics = Topic.objects.filter(module__in=modules)
	
	return render(request, "ELearn/course_home.html", {"course": course, "modules":modules, "topics":topics})

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

def delete_topic(request, topic_id):	
	
	topic = Topic.objects.get(pk=topic_id)
	course_id = topic.module.course.course_id
	topic.delete()
	return redirect('coursehome', course_id=course_id)	
	

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
	assessment = Assessment.objects.get(assess_id = assess_id)
	questions_added = Question.objects.filter(assessment = assessment)
	points_added = questions_added.aggregate(Sum('question_points'))
	if request.method == 'POST':
		add_question_form = CreateQuestions(request.POST)
		add_question_form.instance.assessment = Assessment.objects.get(assess_id = assess_id)		
		add_question_form.save()
		messages.success(request, f'✔️ Question added')
		add_question_form = CreateQuestions()
		points_added = Question.objects.filter(assessment = assessment).aggregate(Sum('question_points'))
		return render(request, "ELearn/add_questions.html", {"form" : add_question_form, "assessment":assessment, "questions_added":questions_added, "points_added":points_added})	
	
	return render(request, "ELearn/add_questions.html", {"form" : add_question_form, "assessment":assessment, "questions_added":questions_added, "points_added":points_added})

def module_home(request, module_id):

	module = Module.objects.get(module_id=module_id)
	return render(request, "ELearn/module_home.html", {"module":module})

def assessment_home(request, module_id):

	assessment = Assessment.objects.get(module=module_id)
	questions = Question.objects.filter(assessment=assessment.assess_id)
	is_published = assessment.is_published
	return render(request, "ELearn/assessment_home.html", {"questions":questions, "module_id":module_id, "is_published":is_published, "assess_id":assessment.assess_id})

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
	return render(request, "ELearn/assessment_home.html", {"questions":questions, "module_id":module_id, "is_published":assessment.is_published, "assess_id":assessment.assess_id})

def view_student_stats(request, module_id):
	assessment = Assessment.objects.get(module=module_id)
	assess_attempts = Assessment_Attempt.objects.filter(assessment=assessment.assess_id)
	student_scores = Assessment_Attempt.objects.filter(assessment=assessment.assess_id).values('attempt_user__first_name','attempt_user__last_name', 'attempt_user__username').annotate(Sum('result'))
	return render(request, "ELearn/student_stats.html", {"assessment":assessment, "assess_attempts":assess_attempts, "student_scores":student_scores})


def upload_questions(request, assess_id):

	current_assessment = Assessment.objects.get(assess_id = assess_id)

	if request.method == 'POST':
		files = request.FILES

		try:
			excel_file = request.FILES['files']
	
			if (str(excel_file).split('.')[-1] == "xlsx"):
				data = xlsx_get(excel_file, column_limit=9)
				assessments = data["Assessment"]

				if (len(assessments) > 1):

					for assessment in assessments:

						if (len(assessment) > 0): 

							# It is not a header row
							if (assessment[0] != "No"): 
								
								# Check if data length is less than 8 

								if (len(assessment) == 9):								
								
									Question.objects.create(question_text = assessment[2], 
														answer_text = assessment[3],
    													question_type = assessment[1],
        											    question_points = assessment[8],
    													option_a = assessment[4],
    													option_b = assessment[5],
    													option_c = assessment[6],
    													option_d = assessment[7],
    													assessment = current_assessment)
					messages.success(request, f'✔️ Assessment uploaded')
					questions = Question.objects.filter(assessment=current_assessment.assess_id)
					is_published = current_assessment.is_published
					return render(request, "ELearn/assessment_home.html", {"questions":questions, "module_id":current_assessment.module, "is_published":is_published, "assess_id":current_assessment.assess_id})
		
		except MultiValueDictKeyError:
			return redirect('home')

	return render(request, "ELearn/upload_questions.html", {"assessment":current_assessment})

def delete_question(request, ques_id):
	question = Question.objects.get(pk=ques_id)
	current_assessment = question.assessment
	question.delete()
	questions = Question.objects.filter(assessment=current_assessment.assess_id)
	current_assessment.is_published = False
	current_assessment.save()
	is_published = current_assessment.is_published
	return render(request, "ELearn/assessment_home.html", {"questions":questions, "module_id":current_assessment.module, "is_published":is_published, "assess_id":current_assessment.assess_id})
		

def compose_message(request):
	create_message_form = CreateMessage()

	if request.method == 'POST':

		create_message_form = CreateMessage(request.POST)
		create_message_form.save(False)

		receivers = create_message_form.instance.receivers.split(';')

		for receiver in receivers:

			to_user = User.objects.get(username=receiver)

			if to_user == '':
				to_user = User.objects.get(email=receiver)

			Message.objects.create(sender=request.user, receiver=to_user, receivers=receivers,
										msg_subject=create_message_form.instance.msg_subject,
										msg_content=create_message_form.instance.msg_content)
			
		messages.success(request, f'✔️ Message sent!')
		mailbox = Message.objects.filter(receiver=request.user)
		return render(request, "ELearn/inbox.html", { "mailbox": mailbox})
	return render(request, "ELearn/compose_message.html", { "form":create_message_form })

def inbox(request):
	mailbox = Message.objects.filter(receiver=request.user)
	return render(request, "ELearn/inbox.html", { "mailbox": mailbox})

def sent_items(request):
	sent_items = Message.objects.filter(sender=request.user)
	return render(request, "ELearn/sent_items.html", { "sent_items": sent_items})

def create_discussion(request):
	create_discussion_form = CreateDiscussion()
	if request.method == 'POST':
		create_discussion_form = CreateDiscussion(request.POST)
		create_discussion_form.save(False)
		create_discussion_form.instance.user = request.user
		create_discussion_form.save()
		messages.success(request, f'✔️ Discussion has been created')
		discussions = Comment.objects.all().order_by('topic')
		return render(request, "ELearn/discussions.html", { "discussions":discussions })
	return render(request, "ELearn/create_discussion.html", { "form":create_discussion_form })

def post_comment(request, topic):	
	post_comment_form = PostComment()

	if request.method == 'POST':
		post_comment_form = PostComment(request.POST)
		post_comment_form.save(False)
		Comment.objects.create(topic=topic, content=post_comment_form.instance.content, user=request.user)
		discussions = Comment.objects.all().order_by('topic')
		return render(request, "ELearn/discussions.html", { "discussions":discussions })

	discussion = Comment.objects.filter(topic=topic)
	return render(request, "ELearn/post_comment.html", { "form":post_comment_form, "topic":topic, "discussion":discussion })

def view_discussion(request):
	discussions = Comment.objects.all().order_by('topic')
	return render(request, "ELearn/discussions.html", { "discussions":discussions })

def create_assignment(request, course_id):
	create_assignment_form = CreateAssignment()
	course = Course.objects.get(course_id=course_id)

	if request.method == 'POST':
		create_assignment_form = CreateAssignment(request.POST)
		assignment = create_assignment_form.save(False)
		module = Module(module_name = assignment.assign_name, module_type = 'AT', course=course)
		module.save()
		create_assignment_form.instance.module = module.module_id
		create_assignment_form.instance.course = course
		assignment = create_assignment_form.save()
		messages.success(request, f'✔️ Assignment created')
		return render(request, "ELearn/assignment_home.html", {"assignment":assignment})

	return render(request, "ELearn/create_assignment.html", {"form" : create_assignment_form, "course_id":course_id})

def assignment_home(request, module_id):
	assignment = Assignment.objects.get(module=module_id)
	return render(request, "ELearn/assignment_home.html", {"assignment":assignment, "module_id":module_id})


def create_project(request, course_id):
	create_project_form = CreateProject()
	course = Course.objects.get(course_id=course_id)

	if request.method == 'POST':
		create_project_form = CreateProject(request.POST)
		project = create_project_form.save(False)
		module = Module(module_name = project.project_name, module_type = 'PT', course=course)
		module.save()
		create_project_form.instance.module = module.module_id
		create_project_form.instance.course = course
		project = create_project_form.save()
		messages.success(request, f'✔️ Project created')
		return render(request, "ELearn/project_home.html", {"project":project})

	return render(request, "ELearn/create_project.html", {"form" : create_project_form, "course_id":course_id})

def project_home(request, module_id):
	project = Project.objects.get(module=module_id)
	return render(request, "ELearn/project_home.html", {"project":project, "module_id":module_id})

