from django.conf.urls import url
from django.conf import settings
from django.views.generic import RedirectView
from accounts.views import UserDetailView, ChangePasswordView

_urlpatterns = [
    url('^$', 'accounts.views.index', name='index'),
    url('^login/$', RedirectView.as_view(pattern_name='account:index'), 
        name='login'),
    url('^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 
        name='logout'), 
    url('^register/$', 'accounts.views.register', name='register'),
    url('^edit/$', UserDetailView.as_view(), name='edit'),
    url('^forgot/$', 'accounts.views.forgot', name='forgot_password'),
    url('^forgot/(?P<code>[a-f0-9]{32})$', 'accounts.views.forgot_reset', 
        name='forgot_reset'),
    url('^confirm-account/$', 'accounts.views.social_confirm',
        name='social_confirm'),
    url('^verify_new_email$', 'accounts.views.verify_new_email',
        name='verify_new_email'),
    url('^verify/(?P<code>[a-f0-9]{32})$', 'accounts.views.verify_email', 
        name='verify_email'),
    url('^change-password/$', ChangePasswordView.as_view(),
        name='change_password'),
]


if settings.DEBUG:
    _urlpatterns.extend([
        url('^promote-user$', 'accounts.views.promote_user'),
        url('^debug$', 'accounts.views.debug_page')
    ])


def urls(namespace='account'):
    """Returns a 3-tuple for use with include().

    The including module or project can refer to urls as namespace:urlname,
    internally, they are referred to as app_name:urlname.
    """
    return (_urlpatterns, 'account', namespace)

