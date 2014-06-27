from django.conf.urls import patterns, url

from forum import views

urlpatterns = patterns('',
    url(r'^$', views.index_view, name='index'),
    url(r'^categories/(?P<pk>\d+)/', views.category_view, name='category'),
    url(r'^threads/(?P<pk>\d+)/', views.thread_view, name='thread'),
    url(r'^follow/', views.follow_view, name='follow'),
    url(r'^unfollow/', views.unfollow_view, name='unfollow'),
    url(r'^new_thread/(?P<category_id>\d+)/', views.new_thread_view, name='new_thread'),
    url(r'^new_post/(?P<thread_id>\d+)/', views.new_post_view, name='new_post'),
    url(r'^new_comment/(?P<post_id>\d+)/', views.new_comment_view, name='new_comment'),
    url(r'^up_post/', views.up_post_view, name='up_post'),
    url(r'^up_comment/', views.up_comment_view, name='up_comment'),
)
