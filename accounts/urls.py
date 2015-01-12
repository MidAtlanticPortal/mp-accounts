from django.conf.urls import patterns, include, url
from django.conf import settings

urlpatterns = patterns('',
    url('^$', 'accounts.views.index', name='index'),
    url('^login/$', 'accounts.views.login_page', name='login'),
    url('^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 
        name='logout'), 
    url('^validate$', 'accounts.views.validate_your_email', 
        name='validate_email_message'),

    url('^invalid/$', 'accounts.views.invalid_credentials', 
        name='invalid_credentials'),
)


if settings.DEBUG:
    urlpatterns += patterns('',
        url('^promote-user$', 'accounts.views.promote_user'),
    )
