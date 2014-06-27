from django.conf.urls import patterns, url

from modules import views

urlpatterns = patterns('',
    url(r'^$', views.index_modules_view, name='index'),
    url(r'^register/(?P<mod_name>.+)/(?P<act_name>.+)/', views.register_view, name='register'),
    url(r'^unregister/(?P<mod_name>.+)/(?P<act_name>.+)/', views.unregister_view, name='unregister'),
    url(r'^(?P<mod_name>.+)/(?P<act_name>.+)/', views.module_view, name='module'),
)
