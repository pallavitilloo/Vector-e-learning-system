from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from ELearn.models import Module, Topic, Assessment, Question

class CreateModuleForm(forms.ModelForm):

    class Meta:
        model = Module        
        fields = ['module_type','module_name', 'module_desc','course']
        exclude = ('course',)

class CreateTopicForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ['topic_type', 'topic_url', 'topic_file', 'module']
        exclude = ('module',)