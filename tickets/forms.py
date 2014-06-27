from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from django_doge.decorators.forms import labels_as_placeholders
from auth.models import DogeUser
from tickets.models import Ticket, Response

from random import choice
import datetime

PRIORITIES = (
    (1, _('Critical')),
    (2, _('High')),
    (3, _('Normal')),
    (4, _('Low')),
    (5, _('Very Low')),
)

@labels_as_placeholders
class TicketForm(forms.ModelForm):
    title = forms.CharField(max_length=50, label=_('Title'))
    problem = forms.CharField(max_length=2000,
                              widget=forms.Textarea,
                              label=_('Problem'))
    priority = forms.ChoiceField(choices=PRIORITIES,
                                 widget=forms.Select(attrs={'multiple' : None}),
                                 initial=3)

    class Meta:
        model = Ticket
        fields = (
            'title',
            'problem',
            'priority',
        )

    def create_ticket(self, doge_user, user):
        admins = User.objects.filter(is_staff=True)
        new_ticket = Ticket(
            author=doge_user,
            title=self.cleaned_data.get('title'),
            priority=self.cleaned_data.get('priority'),
            assigned_to=choice(admins),
            pub_date=datetime.datetime.now(),
        )
        new_ticket.save()
        new_response = Response(
            author=user,
            linked_to=new_ticket,
            response=self.cleaned_data.get('problem'),
            pub_date=datetime.datetime.now(),
        )
        new_response.save()
        return new_ticket

@labels_as_placeholders
class ResponseForm(forms.ModelForm):
    response = forms.CharField(max_length=2000,
                               widget=forms.Textarea,
                               label=_('Reply'))

    class Meta:
        model = Response
        fields = (
            'response',
        )

    def response_to(self, user, ticket_id):
        try:
            ticket = Ticket.objects.get(id=ticket_id)
        except ObjectDoesNotExist:
            return None
        new_response = Response(
            author=user,
            linked_to=ticket,
            response=self.cleaned_data.get('response'),
            pub_date=datetime.datetime.now(),
        )
        new_response.save()
        return new_response
