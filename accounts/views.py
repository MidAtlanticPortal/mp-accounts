from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from social.backends.google import GooglePlusAuth

@login_required
def index(request):
    """Serve up the primary account view, or the login view.
    """
    return render(request, 'accounts/index.html')

def login(request):
    """Serve up the primary account view, or the login view.
    """
    c = dict(GPLUS_ID=settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY, 
             GPLUS_SCOPE=' '.join(settings.SOCIAL_AUTH_GOOGLE_PLUS_SCOPES))
    
    return render(request, 'accounts/login.html', c)
