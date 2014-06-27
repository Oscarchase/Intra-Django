from django import template
from django.utils.translation import ugettext as _

register = template.Library()

PRIORITY_CLASSES = (
    'label-danger',
    'label-warning',
    'label-info',
    'label-success',
    'label-primary',
)

PRIORITY_NAMES = (
    _('Critical'),
    _('High'),
    _('Normal'),
    _('Low'),
    _('Very Low'),
)

@register.filter(name='priority_class')
def priority_class(priority):
    return PRIORITY_CLASSES[priority - 1]

@register.filter(name='priority_name')
def priority_name(priority):
    return PRIORITY_NAMES[priority - 1]
