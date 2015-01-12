from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from social.backends.google import GooglePlusAuth
from django.contrib.sessions.models import Session
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.http.response import Http404, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.urlresolvers import reverse


def index(request):
    """Serve up the primary account view, or the login view.
    """
    if request.user.is_anonymous():
        return login_page(request)
    
    c = {}

    if settings.DEBUG:
        c['users'] = User.objects.all()
        c['sessions'] = all_logged_in_users()

    return render(request, 'accounts/index.html', c)

def login_page(request):
    """Serve up the primary account view, or the login view.
    """
    next_page = request.GET.get('next', '/')
    c = {}
    
    if request.method == 'POST': 
        # Try a user/pw login
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        if user is not None: 
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next_page)
            else:
                return HttpResponse("Access Denied", status=403)
        else:
            # bad password
            return HttpResponseRedirect(reverse('account:invalid_credentials'))

       
    c = dict(GPLUS_ID=settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY, 
             GPLUS_SCOPE=' '.join(settings.SOCIAL_AUTH_GOOGLE_PLUS_SCOPES),
             next=next_page)
    
    return render(request, 'accounts/login.html', c)


def validate_your_email(request):
    return HttpResponse("Check your email and validate to continue", 
                        content_type='text/plain')

def invalid_credentials(request):
    return HttpResponse("Those credentials will not provide you access to _this_ website.\n\nPerhaps you'd like to sign up for an account?", 
                        content_type='text/plain')

def all_logged_in_users():
    sessions = Session.objects.filter(expire_date__gte=timezone.now())
    users = []
    for session in sessions:
        uid = session.get_decoded().get('_auth_user_id', None)
        if uid: 
            user_obj = User.objects.filter(id=uid)
            if user_obj:
                users.append({'user': user_obj[0], 'until': session.expire_date})
    
    return users


if settings.DEBUG:
    from django.http import HttpResponse

    def promote_user(request):
        """Promote the current user to staff status
        """
        request.user.is_staff = True
        request.user.is_superuser = True
        request.user.save()
        return HttpResponse('You are now staff+superuser', content_type='text/plain', status=200)

        

