from django import template

register = template.Library()

from correcting.models import Rank

@register.filter(name='rank_panel_class')
def rank_panel_class(rank):
    if rank is None:
        return 'panel-info'
    if rank.value == Rank.RANK_FAIL:
        return 'panel-danger'
    return 'panel-success'

@register.filter(name='rank_str')
def rank_string(rank):
    return Rank.RANKS[rank.value][1]
