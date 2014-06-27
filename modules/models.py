from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

from auth.models import DogeUser
from forum.models import Category

class Registerable(models.Model):
    places = models.IntegerField()
    start = models.DateTimeField()
    end = models.DateTimeField()
    register_start = models.DateTimeField()
    register_end = models.DateTimeField()
    registered = models.ManyToManyField(DogeUser)

    @property
    def is_closed_for_registration(self):
        return timezone.now() > self.register_end

    @property
    def is_full(self):
        return self.registered.count() >= self.places

    @property
    def can_register(self):
        return not self.is_closed_for_registration and not self.is_full

class Module(Registerable):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=2000)
    credits = models.IntegerField()

    def __str__(self):
        return self.name

class Activity(Registerable):
    PROJECT = 0
    EXAM = 1
    TD = 2
    TYPES = (
        (PROJECT, _('project')),
        (EXAM, _('exam')),
        (TD, _('td')),
    )

    module = models.ForeignKey(Module)
    name = models.CharField(max_length=100)
    type = models.IntegerField(choices=TYPES)
    description = models.CharField(max_length=2000)
    subject = models.FileField(
        upload_to=lambda instance,
        filename: filename, blank=True, null=True
    )
    group_size = models.IntegerField()
    peer_number = models.IntegerField()

    def __str__(self):
        return '%s (%s)' % (self.name, self.module)

class Group(models.Model):
    name = models.CharField(max_length=50)
    activity = models.ForeignKey(Activity)
    group_leader = models.ForeignKey(DogeUser, related_name="group_leader")
    group_members = models.ManyToManyField(DogeUser, related_name="group_members",
                                           default=None, blank=True, null=True)
    git_link = models.CharField(max_length=100)

    def __str__(self):
        return '%s (%d)' % (self.name, self.group_members.count())

@receiver(post_save)
def on_module_post_save(sender, **kwargs):
    """Automatically creates:

    - a forum category for a new module
    - a forum subcategory for a new activity
    """
    if sender is Module:
        try:
            Category.objects.get(title=kwargs['instance'].name)
        except Category.DoesNotExist:
            forum_categroy = Category(title=kwargs['instance'].name)
            forum_categroy.save()
    elif sender is Activity and kwargs['instance'].type == Activity.PROJECT:
        module_name = kwargs['instance'].module.name
        try :
            module_category = Category.objects.get(title=module_name)
        except Category.DoesNotExist:
            return
        try:
            Category.objects.get(title=kwargs['instance'].name)
        except Category.DoesNotExist:
            forum_categroy = Category(
                title=kwargs['instance'].name,
                sub_category=module_category
            )
            forum_categroy.save()
