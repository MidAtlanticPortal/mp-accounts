from django.conf.urls import url, include
import accounts.urls
from django.http import HttpResponse

urlpatterns = [
    url(r'^foo/', lambda request: HttpResponse('FOO')),
    url(r'^account/', include(accounts.urls.urls(namespace='account'))),
]
