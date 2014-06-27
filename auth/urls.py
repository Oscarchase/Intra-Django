from django.conf.urls import patterns, include, url

from auth import views

urlpatterns = patterns('',
    url(r'^$', views.login_view, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
)
