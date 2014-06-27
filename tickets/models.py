from django.db import models
from django.contrib.auth.models import User

from auth.models import DogeUser

class Ticket(models.Model):
    author = models.ForeignKey(DogeUser)
    title = models.CharField(max_length=50)
    priority = models.IntegerField(default=3)
    assigned_to = models.ForeignKey(User)
    pub_date = models.DateTimeField('date published')
    is_active = models.BooleanField(default=1)

    def __str__(self):
        return self.title

class Response(models.Model):
    author = models.ForeignKey(User)
    linked_to = models.ForeignKey(Ticket)
    response = models.CharField(max_length=2000)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.response[:50]
