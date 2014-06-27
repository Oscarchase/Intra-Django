from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _

from auth.models import DogeUser

from uuid import uuid4

def autologin_view(request, token):
    try:
        doge_user = DogeUser.objects.get(autologin=token)
    except ObjectDoesNotExist:
        return HttpResponseForbidden(_('Invalid autologin token'))
    if request.user.is_authenticated():
        logout(request)
    # Faking authenticate before login
    # (http://stackoverflow.com/a/2787747/1592289)
    doge_user.user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, doge_user.user)
    next_url = request.GET.get('next', '/')
    return HttpResponseRedirect(next_url)

@login_required
def regenerate_view(request):
    while True:
        uid = uuid4().hex
        try:
            DogeUser.objects.get(autologin=uid)
        except ObjectDoesNotExist:
            break
    try:
        doge_user = DogeUser.objects.get(user_id=request.user.id)
    except ObjectDoesNotExist: # Fatal error (user not linked to DogeUser)
        return HttpResponseForbidden(_('You are not a doge user'))
    doge_user.autologin = uid
    doge_user.save()
    next_url = request.GET.get('next', '/')
    return HttpResponseRedirect(next_url)
