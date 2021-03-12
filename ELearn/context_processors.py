from ELearn.models import Course, User

def get_courses(request):
    course_list = []
    if request.user.is_authenticated:
        current_user = request.user
        course_list = Course.objects.filter(instructor=current_user)
        
    return{
        'CURRENT_USER_COURSES' : course_list,         
    }