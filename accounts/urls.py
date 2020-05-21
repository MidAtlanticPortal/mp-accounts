try:
    from django.urls import re_path, include
except ModuleNotFoundError as e:
    from django.conf.urls import url as re_path, include
from django.conf import settings
from django.views.generic import RedirectView
from accounts.views import UserDetailView, ChangePasswordView
from . import views
from django.contrib import auth

app_name = 'account'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^login/$', RedirectView.as_view(pattern_name='account:index'),
        name='login'),
    re_path(r'^logout/$', auth.logout, {'next_page': '/'},
        name='logout'),
    re_path(r'^register/$', views.register, name='register'),
    re_path(r'^edit/$', UserDetailView.as_view(), name='edit'),
    re_path(r'^forgot/$', views.forgot, name='forgot_password'),
    re_path(r'^forgot/(?P<code>[a-f0-9]{32})$', views.forgot_reset,
        name='forgot_reset'),
    re_path(r'^confirm-account/$', views.social_confirm,
        name='social_confirm'),
    re_path(r'^verify_new_email$', views.verify_new_email,
        name='verify_new_email'),
    re_path(r'^verify/(?P<code>[a-f0-9]{32})$', views.verify_email,
        name='verify_email'),
    re_path(r'^change-password/$', ChangePasswordView.as_view(),
        name='change_password'),
]


if settings.DEBUG:
    urlpatterns.extend([
        re_path(r'^promote-user$', views.promote_user),
        re_path(r'^debug$', views.debug_page)
    ])


def urls(namespace='account'):
    """Returns a 3-tuple for use with include().

    The including module or project can refer to urls as namespace:urlname,
    internally, they are referred to as app_name:urlname.
    """
    return (urlpatterns, 'account', namespace)
