from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_doge.decorators.auth import doge_user_required
from urllib.parse import unquote
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from django.views.decorators.http import require_POST

from auth.models import DogeUser
from modules.models import Module, Activity, Group

import json

@login_required
def index_modules_view(request):
    return render(request, 'modules/index.html')

@doge_user_required
def module_view(request, act_name, mod_name):
    activity = get_object_or_404(Activity, name=unquote(act_name))
    cur_module = get_object_or_404(Module, name=unquote(mod_name))
    doge_user = DogeUser.objects.get(user=request.user)
    registered_users = DogeUser.objects.exclude(registerable__in=[activity])
    cur_group = None
    if activity.group_size > 1 and doge_user in activity.registered.all():
        cur_group = get_object_or_404(Group,
            group_leader=DogeUser.objects.get(user=request.user),
            activity=activity,
        )
    return render(request, 'modules/module.html', {
        'activity': activity,
        'doge_user' : DogeUser.objects.get(user=request.user),
        'registered_users' : registered_users,
        'cur_group' : cur_group,
        'module' : cur_module,
    })

@doge_user_required
def unregister_view(request, mod_name, act_name):
    return registration(request, unquote(act_name),
        unquote(mod_name), unregister_one, unregister_group, request.POST)

@doge_user_required
def register_view(request, mod_name, act_name):
    return registration(request, unquote(act_name),
        unquote(mod_name), register_one, register_group, request.POST)

def registration(request, act_name, mod_name, register_func, register_group_func, group_infos):
    doge_user = DogeUser.objects.get(user=request.user)
    cur_activity = Activity.objects.get(name=act_name)
    cur_module = Module.objects.get(name=mod_name)
    end_of_registration = cur_activity.register_end
    if end_of_registration > timezone.now():
        if cur_activity.group_size == 1:
            register_func(cur_activity, cur_module, doge_user)
        elif cur_activity.group_size > 1:
            register_group_func(cur_activity, cur_module, doge_user, group_infos)
    return redirect('modules:module', act_name=act_name, mod_name=cur_activity.module.name)

DOGESPHERE_LINK = lambda activity, user:\
    'dogesphere@dogesphere.doge.fr:%s/%s/%s' %\
    (activity.module, activity.name, user)

def register_one(cur_activity, cur_module, doge_user):
    new_group = Group(
        name='%s %s' % (cur_activity.name, doge_user),
        activity=cur_activity,
        group_leader=doge_user,
        git_link=DOGESPHERE_LINK(cur_activity, doge_user),
    )
    new_group.save()
    new_group.group_members.add(doge_user)
    if doge_user not in cur_module.registered.all():
        cur_module.registered.add(doge_user)
    cur_activity.registered.add(doge_user)

def unregister_one(cur_activity, cur_module, doge_user):
    group_to_delete = Group.objects.get(
        group_leader=doge_user,
        activity=cur_activity,
    )
    group_to_delete.delete()
    cur_activity.registered.remove(doge_user)
    cur_module.registered.remove(doge_user)

def register_group(cur_activity, cur_module, doge_user, group_infos):
    if doge_user in cur_activity.registered.all():
        unregister_group(cur_activity, cur_module, doge_user, group_infos)
    new_group = Group(
        name=group_infos['group_name'],
        activity=cur_activity,
        group_leader=doge_user,
        git_link=DOGESPHERE_LINK(cur_activity, doge_user),
    )
    new_group.save()
    for login in json.loads(group_infos['group_members']):
        user = get_object_or_404(DogeUser, login=login)
        new_group.group_members.add(user)
        if user not in cur_module.registered.all():
            cur_module.registered.add(user)
        cur_activity.registered.add(user)

def unregister_group(cur_activity, cur_module, doge_user, group_infos):
    group_to_delete = Group.objects.get(
        name=group_infos['group_name'],
        activity=cur_activity,
        group_leader=doge_user,
        git_link=DOGESPHERE_LINK(cur_activity, doge_user),
    )
    for user in group_to_delete.group_members.all():
        cur_activity.registered.remove(user)
        cur_module.registered.remove(user)
    group_to_delete.delete()
