from django.conf.urls import url, include

urlpatterns = [
    url(r'^a/', include('accounts.urls')),
]
