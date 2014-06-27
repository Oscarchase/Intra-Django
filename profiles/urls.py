from django.conf.urls import patterns, url

from profiles import views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name='index'),
    url(r'^(?P<login>[a-zA-Z\-]+)$', views.user_view, name='user'),
    url(r'^picture/(?P<login>[a-zA-Z\-]+)/', views.api_picture_view, name='picture'),
)
