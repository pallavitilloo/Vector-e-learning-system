from ELearn.models import Course, User

def get_courses(request):
    courseList = []
    # if request.user.is_authenticated:
    #     currentUserProfile = request.user.profile        
    #     courseList = currentUserProfile.courses.all()
        
    return{
        'CURRENT_USER_COURSES' : courseList,         
    }