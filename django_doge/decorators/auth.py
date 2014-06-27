from django.contrib.auth.decorators import login_required, user_passes_test

from auth.models import DogeUser

def check_doge_user(user):
    try:
        DogeUser.objects.get(login=user.username)
        return True
    except DogeUser.DoesNotExist:
        return False

def doge_user_required(view_func):

    @login_required
    @user_passes_test(check_doge_user)
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)

    return wrapper
