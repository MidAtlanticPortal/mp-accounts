from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url('^$', 'accounts.views.index', name='index'),
    url('^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 
        name='logout'), 
    url('^register/$', 'accounts.views.register', name='register'),
    url('^confirm-email/$', 'accounts.views.social_confirm_email', name='social_confirm_email'),
    url('^verify_new_email$', 'accounts.views.verify_new_email', name='verify_new_email'),
    url('^verify/(?P<code>[a-f0-9]{32})$', 'accounts.views.verify_email', 
        name='verify_email'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url('^promote-user$', 'accounts.views.promote_user'),
    )
