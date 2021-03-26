from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from ELearn.models import Module, Topic, Assessment, Question, Assessment_Attempt, Message

class CreateModuleForm(forms.ModelForm):

    class Meta:
        model = Module        
        fields = ['module_type','module_name', 'module_desc','course']
        exclude = ('course','module_type')

class CreateTopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['topic_type', 'topic_url', 'topic_file', 'module']
        exclude = ('module',)

class CreateAssessmentForm(forms.ModelForm):

    class Meta:
        model = Assessment
        fields = ['assess_name','assess_points','assess_time_limit','course','module','is_published']
        exclude = ('course', 'module','is_published')
    
    def __init__(self, *args, **kwargs):
        super(CreateAssessmentForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['assess_name'].widget.attrs['readonly'] = True

class CreateQuestions(forms.ModelForm):

    class Meta:
        model = Question
        fields = ['assessment','question_points','question_type','question_text', 'answer','answer_text', 'option_a','option_b','option_c','option_d']
        exclude = ('assessment','answer')

class CreateAssessmentAttempt(forms.ModelForm):

    class Meta:
        model = Assessment_Attempt
        fields = ['attempt_user','assessment','question','answer','result']
        exclude = ()

class CreateMessage(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['sender','receiver','receivers','msg_subject','msg_content','created_at']
        exclude = ('sender','created_at','receiver')