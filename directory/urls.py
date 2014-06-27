from django.conf.urls import patterns, include, url

from directory import views

urlpatterns = patterns('',
    url(r'^$', views.directory_view, name='index'),
)
