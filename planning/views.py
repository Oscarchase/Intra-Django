from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseBadRequest
from django_doge.decorators.auth import doge_user_required
from django.db.models import Q

from auth.models import DogeUser
from modules.models import Activity

import json
from datetime import datetime

@doge_user_required
def index_view(request):
    return render(request, 'planning/planning.html')

EVENT_TYPES = {
    Activity.PROJECT : 'event-info',
    Activity.EXAM : 'event-important',
    Activity.TD : 'event-special'
}

@doge_user_required
def data_view(request):
    try:
        date_from = datetime.fromtimestamp(int(request.GET['from'][:-3]))
        date_to = datetime.fromtimestamp(int(request.GET['to'][:-3]))
    except:
        return HttpResponseBadRequest()
    doge_user = DogeUser.objects.get(user=request.user)
    sql_query = (Q(start__lte=date_to) |\
                 Q(end__gte=date_from)) &\
                    Q(registered__in=[doge_user])
    activities = Activity.objects.filter(sql_query)
    calendar_result = list()
    for activity in activities:
        calendar_result.append({
            'id': activity.pk,
            'title': activity.name,
            'url': reverse('modules:module', kwargs={
                'act_name' : activity.name,
                'mod_name' : activity.module.name
            }),
            'class': EVENT_TYPES[activity.type],
            'start': int(activity.start.timestamp() * 1000),
            'end': int(activity.end.timestamp() * 1000),
        })
    return HttpResponse(
        json.dumps({
            'success' : 1,
            'result' : calendar_result
        }),
        content_type='application/json'
    )
