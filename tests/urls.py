from django.conf.urls import url, include
import accounts.urls
from django.http import HttpResponse

fake_social = [
    url(r'^b/(?P<x>.*)$', lambda request, x: HttpResponse('b'), name='begin'),
    url(r'^c/(?P<x>.*)$', lambda request, x: HttpResponse('c'), name='complete'),
]

urlpatterns = [
    url(r'^foo/', lambda request: HttpResponse('FOO')),
    url(r'^soc/', include(fake_social, namespace='social')),
    url(r'^account/', include(accounts.urls.urls(namespace='account'))),
]
