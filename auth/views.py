from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout

from auth.forms import LoginForm
from auth.models import DogeUser

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth:login'))

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(username=request.POST['username'],
                                password=request.POST['password'])
            # Authenticated and not banned
            if user is not None and user.is_active:
                login(request, user)
                # Linking DogeUser and Django's user models
                try:
                    doge_user = DogeUser.objects.get(user_id=user.id)
                except ObjectDoesNotExist:
                    try:
                        doge_user = DogeUser.objects.get(login=user.username)
                        doge_user.user = user
                        doge_user.save()
                    except ObjectDoesNotExist:
                        # Link failed (not listed in ldap)
                        pass
                # Handling a possible redirection
                next_url = request.POST.get('next', reverse('index'))
                return HttpResponseRedirect(next_url)
    else:
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('index'))
        form = LoginForm()
    return render(request, 'auth/login.html', {'form': form})
