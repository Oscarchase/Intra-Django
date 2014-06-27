from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from elearning.models import ELearningResource
from modules.models import Module, Activity

from urllib.parse import unquote

@login_required
def index_view(request):
    return render(request, 'elearning/index.html')

@login_required
def activity_view(request, activity_name):
    activity = get_object_or_404(Activity, name=unquote(activity_name))
    resources = ELearningResource.objects.filter(project=activity)
    return render(request, 'elearning/index.html', {
        'activity' : activity,
        'resources' : resources,
    })
