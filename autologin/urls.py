from django.conf.urls import patterns, url

from autologin import views

urlpatterns = patterns('',
    url(r'^(?P<token>[0-9A-Fa-f]{32})/', views.autologin_view, name='autologin'),
    url(r'^regenerate/', views.regenerate_view, name='regenerate'),
)
