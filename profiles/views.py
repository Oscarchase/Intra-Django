from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, NoReverseMatch
from django.contrib.auth.decorators import login_required

from auth.models import DogeUser
from modules.models import Module, Activity
from correcting.models import Grade, Rank

@login_required
def index_view(request):
    try:
        query = request.GET['query']
        try:
            profile_url = reverse('profiles:user', kwargs={'login':query})
            return HttpResponseRedirect(profile_url)
        except NoReverseMatch:
            # invalid login pattern
            pass
    except KeyError:
        pass
    # Redirect user to the referer page (defaulting to the index if none)
    referer = request.META.get('HTTP_REFERER', reverse('index'))
    return HttpResponseRedirect(referer)

@login_required
def user_view(request, login):
    user = get_object_or_404(DogeUser, login=login)
    modules = Module.objects.filter(registered__in=[user])
    activities = dict()
    grades = dict()
    ranks = dict()
    credits_acquired = 0
    credits_progress = 0
    for module in modules:
        module_activities = Activity.objects.filter(
            module=module,
            type__in=[Activity.PROJECT, Activity.EXAM]
        ).order_by('-type', 'end')
        activities[module] = module_activities
        for activity in module_activities:
            try:
                grades[activity] = Grade.objects.get(activity=activity,
                                                     student=user)
            except (Grade.DoesNotExist, Grade.MultipleObjectsReturned) :
                pass
        try:
            rank = Rank.objects.get(module=module, student=user)
            ranks[module] = rank
            if rank.value != Rank.RANK_FAIL:
                credits_acquired += module.credits
        except Rank.DoesNotExist:
            credits_progress += module.credits
    return render(request, 'profiles/profiles_view.html', {
        'doge_user' : user,
        'modules' : modules,
        'activities' : activities,
        'grades' : grades,
        'ranks' : ranks,
        'credits_acquired' : credits_acquired,
        'credits_progress' : credits_progress,
    })

@login_required
def api_picture_view(request, login):
    user = get_object_or_404(DogeUser, login=login)
    return HttpResponse(user.picture_as_html())
