from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    url('^$', 'accounts.views.index', name='index'),
    url('^login/$', 'accounts.views.login', name='login'),
    url('^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, 
        name='logout'), 
)
