from django.conf.urls import patterns, include, url, i18n
from django.conf.urls.static import static
from django.contrib import admin

from django_doge import views
import forum.urls
import auth.urls
import directory.urls
import tickets.urls
import autologin.urls
import profiles.urls
import planning.urls
import elearning.urls
import modules.urls

from django_doge import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Index page
    url(r'^$', views.index_view, name='index'),
    # Admin panel
    url(r'^admin/', include(admin.site.urls)),
    # Forum
    url(r'^forum/', include(forum.urls, namespace='forum')),
    # Authentication
    url(r'^login/', include(auth.urls, namespace='auth')),
    # LDAP directory
    url(r'^ldap/', include(directory.urls, namespace='directory')),
    # Ticketing system
    url(r'^tickets/', include(tickets.urls, namespace='tickets')),
    # Autologin
    url(r'^autologin/', include(autologin.urls, namespace='autologin')),
    # Profiles
    url(r'^profiles/', include(profiles.urls, namespace='profiles')),
    # Planning
    url(r'^planning/', include(planning.urls, namespace='planning')),
    # E-learning
    url(r'^e-learning/', include(elearning.urls, namespace='e-learning')),
    # Modules
    url(r'^modules/', include(modules.urls, namespace='modules')),
    # Internationalization
    url(r'^i18n/', include(i18n)),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = views.not_found_view
