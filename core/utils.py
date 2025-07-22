from .models import UserProfile

def redirect_url(request,admin,user,mio):
    if request.user.is_superuser:
        return admin
    try:
        profile = request.user.userprofile
        if profile.user_type == 'zone' or profile.user_type == 'region':
            return user
        else:
            return mio
    except UserProfile.DoesNotExist:
        return mio
