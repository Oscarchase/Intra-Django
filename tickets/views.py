from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _
from django.contrib import messages

from tickets.models import Ticket, Response
from tickets.forms import TicketForm, ResponseForm
from auth.models import DogeUser


@login_required
def index_view(request):
    try:
        doge_user = DogeUser.objects.get(user=request.user)
        tickets = Ticket.objects.filter(author=doge_user)
    except ObjectDoesNotExist:
        tickets = Ticket.objects.filter(assigned_to=request.user)
    responses = dict()
    superusers = User.objects.filter(is_superuser=True)
    for ticket in tickets:
        responses[ticket] = Response.objects.filter(linked_to=ticket)
    return render(request, 'tickets/index.html', {
        'tickets': tickets,
        'creation_form': TicketForm(),
        'response_form': ResponseForm(),
        'responses': responses,
        'superusers': superusers,
    })

def index_redirect(fragment):
    url = '%s#%s' % (reverse('tickets:index'), str(fragment))
    return HttpResponseRedirect(url)

@login_required
@require_POST
def new_ticket_view(request):
    try:
        doge_user = DogeUser.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return HttpResponseForbidden(_('You are not a doge user'))
    form = TicketForm(data=request.POST)
    if form.is_valid():
        ticket = form.create_ticket(doge_user, request.user)
    return index_redirect(ticket.id)

@login_required
@require_POST
def response_to_view(request):
    form = ResponseForm(data=request.POST)
    if form.is_valid():
        form.response_to(request.user, request.POST['ticket_id'])
        return index_redirect(request.POST['ticket_id'])
    return HttpResponseRedirect(reverse('index'))

@login_required
@require_POST
def activation_view(request):
    try :
        ticket_id = request.POST['ticket_id']
    except KeyError:
        return HttpResponseRedirect(reverse('index'))
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.is_active = not ticket.is_active
    ticket.save()
    return index_redirect(ticket.id)

@login_required
@require_POST
def reassign_view(request):
    try :
        superuser = request.POST['superuser']
        ticket_id = request.POST['ticket_id']
    except KeyError:
        return HttpResponseRedirect(reverse('index'))
    assignee = get_object_or_404(User, username=superuser)
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    ticket.assigned_to = assignee
    ticket.save()
    return index_redirect(ticket.id)
