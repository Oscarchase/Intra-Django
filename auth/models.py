from django.db import models
from django.contrib.auth.models import User

class DogeUser(models.Model):
    # Django's user model integration
    user = models.ForeignKey(User, blank=True, null=True)
    # Additional fields
    login = models.CharField(max_length=200, blank=True, null=True)
    mail = models.CharField(max_length=200, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    birth_date = models.DateTimeField('date of birth', blank=True, null=True)
    picture = models.CharField(max_length=20000, blank=True, null=True)
    phone = models.CharField(max_length=200, blank=True, null=True)
    autologin = models.CharField(max_length=32, blank=True, null=True)

    def __str__(self):
        return self.login

    def picture_as_html(self):
        class_name = 'user-picture' if self.picture else 'doge-picture'
        html = '<img class="%s" src="data:image/png;base64,%s">'
        return html % (class_name, self.picture)

    picture_as_html.short_description = 'Picture'
    picture_as_html.allow_tags = True
