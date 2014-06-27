from django.conf.urls import patterns, include, url

from tickets import views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name='index'),
    url(r'^new/', views.new_ticket_view, name='new'),
    url(r'^response/', views.response_to_view, name='response'),
    url(r'^activation/', views.activation_view, name='activation'),
    url(r'^reassign/', views.reassign_view, name='reassign'),
)
