from django.db import models
from django.utils.translation import ugettext as _

from modules.models import Module, Activity
from auth.models import DogeUser

class GradingScale(models.Model):
    project = models.ForeignKey(Activity)

class Grade(models.Model):
    student = models.ForeignKey(DogeUser, related_name='user_student')
    activity = models.ForeignKey(Activity)
    value = models.IntegerField()
    grader = models.ForeignKey(DogeUser, related_name='user_grader')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%d (%s)' % (self.value, self.activity)

class Rank(models.Model):
    RANK_A = 0
    RANK_B = 1
    RANK_C = 2
    RANK_D = 3
    RANK_FAIL = 4
    RANKS = (
        (RANK_A, _('A')),
        (RANK_B, _('B')),
        (RANK_C, _('C')),
        (RANK_D, _('D')),
        (RANK_FAIL, _('FAILING')),
    )

    student = models.ForeignKey(DogeUser)
    module = models.ForeignKey(Module)
    value = models.IntegerField(choices=RANKS)

    def __str__(self):
        return '%s (%s)' % (self.RANKS[self.value], self.module)
