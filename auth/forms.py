from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from django_doge.decorators.forms import labels_as_placeholders

@labels_as_placeholders
class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.error_messages['invalid_login'] = _('Invalid login credentials')

    class Meta:
        model = User
        fields = ('username', 'password')
