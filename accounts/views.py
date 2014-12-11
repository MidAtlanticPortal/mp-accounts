from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    """Serve up the primary account view, or the login view.
    """
    return render(request, 'accounts/index.html')

def login(request):
    """Serve up the primary account view, or the login view.
    """
    return render(request, 'accounts/login.html')
