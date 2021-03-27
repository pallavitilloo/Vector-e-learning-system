from ELearn.models import Course, User, Profile

def get_courses(request):
    course_list = []
    profile_picture_url = ''
    if request.user.is_authenticated:
        current_user = request.user
        course_list = Course.objects.filter(instructor=current_user)
        current_profile = Profile.objects.get(user=current_user)
        profile_picture_url = current_profile.image.url
        
    return{
        'CURRENT_USER_COURSES' : course_list,
        'CURRENT_USER_DP' : profile_picture_url,         
    }