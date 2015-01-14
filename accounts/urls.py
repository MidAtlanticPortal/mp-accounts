from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url('^$', 'accounts.views.index', name='index'),
    url('^login/$', 'accounts.views.login_page', name='login'),
    url('^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 
        name='logout'), 
    url('^register/$', 'accounts.views.register', name='register'),
    url('^verify/(?P<code>[a-f0-9]{32})$', 'accounts.views.verify_email', 
        name='verify_email'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url('^promote-user$', 'accounts.views.promote_user'),
    )
