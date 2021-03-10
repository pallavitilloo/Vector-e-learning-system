from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField("Profile Picture", default="static/OLS/default_user.png", upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username}'

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()

class Course(models.Model):
    course_id = models.CharField("Course ID", max_length=255, blank=False, null=False, unique=True)
    course_name = models.CharField("Course Name", max_length=255, blank=False, null=False, unique=True)
    course_desc = models.TextField("Course Description", blank=True)
    instructor = models.ForeignKey(User, db_column="user", null=True, on_delete=models.SET_NULL)
    days = models.CharField("Day", max_length=255)
    timing = models.CharField("Timing", max_length=255)
    mode = models.CharField("Instruction Mode", max_length=255)
    
    def __str__(self):
        return f'{self.course_id} {self.course_name}'
 
class Module(models.Model):
    module_id = models.AutoField(primary_key=True)
    module_name = models.CharField("Module Name", max_length=255, blank=False, null=False)
    module_desc = models.TextField("Module Description", blank=True)
    module_type = models.CharField("Module Type",
        choices=[('CW','Course Work'),('AS','Assessment'),('AT','Assignment'),('PT','Project')],
        default='CW',
		max_length=24,
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.module_name}'

class Topic(models.Model):
    link_or_file = models.CharField("Link/File", max_length=450, blank=False, null=False)
    topic_type = models.CharField("Type of Topic",
        choices=[('IL','Internal Link'),('EL','External Link'),('FL','File')],
        default='FL',
		max_length=24,
    )
    module = models.ForeignKey(Module, db_column="module_id", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.link_or_file}'

class Assessment(models.Model):
    assess_id = models.AutoField(primary_key=True)
    assess_name = models.CharField("Assessment Name", max_length=255, blank=False, null=False)
    assess_points = models.IntegerField("Assessment Points", blank=False, null=False, default=100)
    assess_time_limit = models.IntegerField("Time limit (mins.)", default=120, blank=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.CharField("Module ID", max_length=255)

    def __str__(self):
        return f'{self.assess_name}'

class Question(models.Model):
    question_id = models.AutoField(primary_key=True)
    question_text = models.TextField("Question", blank=False, null=False)
    answer = models.CharField("Answer",
        choices=[('FI','Fill-in'),('A','Option A'),('B','Option B'),('C','Option C'),('D','Option D')],
        default='FI',
		max_length=24,
    )
    answer_text = models.TextField("Answer", blank=True)
    question_type = models.CharField("Question Type", max_length=30,
        choices=[('FI','Fill-in'),('MCQ','Multiple Choice Question')]
    )
    question_points = models.IntegerField("Points", blank=False, default=0, null=False)
    option_a = models.CharField("Option A", max_length=450)
    option_b = models.CharField("Option B", max_length=450)
    option_c = models.CharField("Option C", max_length=450)
    option_d = models.CharField("Option D", max_length=450)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.question_text}'

class Assessment_Attempt(models.Model):
    attempt_user = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, db_column="question_id", on_delete=models.CASCADE)
    answer = models.TextField("Answer", blank=True)
    result = models.IntegerField("Result", default=0)

    def __str__(self):
        return f'{self.attempt_user} {self.assessment}'

class Assignment(models.Model):
    assign_id = models.AutoField(primary_key=True)
    assign_name = models.CharField("Assignment Name", max_length=255)
    assign_desc = models.TextField("Assignment Description", blank=True)
    assign_points = models.IntegerField("Points",default=100,blank=False)
    deadline = models.DateField("Submission Deadline")
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    module = models.CharField("Module ID", max_length=255)

    def __str__(self):
        return f'{self.assign_name}'

class Submission(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, db_column="user")
    assign_id = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    submission_file = models.CharField("File", max_length=400)

    def __str__(self):
        return f'{self.submission_file}'



