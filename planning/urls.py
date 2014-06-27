from django.conf.urls import patterns, url

from planning import views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name='index'),
    url(r'data/', views.data_view, name='data'),
)
