from django.conf.urls import patterns, url

from elearning import views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name='index'),
    url(r'^(?P<activity_name>.+)/', views.activity_view, name='activity'),
)

