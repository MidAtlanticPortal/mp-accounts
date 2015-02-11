from django.conf.urls import url, include
import accounts.urls

urlpatterns = [
    url(r'^account/', include(accounts.urls.urls(namespace='account'))),
]
