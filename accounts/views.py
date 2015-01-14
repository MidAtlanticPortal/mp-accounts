from django.shortcuts import render, get_object_or_404
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
from forms import SignUpForm
import uuid
from django.template.loader import get_template


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
            return render(request, 'accounts/invalid_credentials.html')

    c = dict(GPLUS_ID=settings.SOCIAL_AUTH_GOOGLE_PLUS_KEY, 
             GPLUS_SCOPE=' '.join(settings.SOCIAL_AUTH_GOOGLE_PLUS_SCOPES),
             next=next_page)
    
    return render(request, 'accounts/login.html', c)

def register(request):
    """Show the registration page.
    """
    
    if not request.user.is_anonymous():
        return HttpResponseRedirect('/')
    
    if request.method == 'POST': 
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            user, created = User.objects.get_or_create(username=username)
            if not created: 
                # TODO: Put this in a view function
                return render(request, 'accounts/registration_error.html')

            validation_code = uuid.uuid4().hex
            
            user.is_active = False  # not validated yet
            user.password = password
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            
            user.save()
            
            # TODO: Store this with the user itself
            # This is a temporary hack to get around having to create a new 
            # user model right now. The problem with this is that the code is 
            # stored in the current session, so use must the same browser 
            # session to validate your email address. In most cases that's 
            # probably fine, but in many cases it won't work. 
             
            request.session['verification_code'] = validation_code
            request.session['user_id'] = user.id
            
            send_verification_email(request, user, validation_code)
            
            return render(request, 'accounts/check_your_email.html')
    else:
        form = SignUpForm()

    c = {
        'form': form,
    }
    return render(request, 'accounts/register.html', c)    


def send_verification_email(request, user, code):
    """Send a verification link to the specified user.
    """
    
    url = request.build_absolute_uri(reverse('account:verify_email', 
                                             args=(code,)))
    
    context = {'name': user.first_name, 'url': url}
    template = get_template('accounts/mail/verify_email.txt')
    body_txt = template.render(context)
    template = get_template('accounts/mail/verify_email.html')
    body_html = template.render(context)
    user.email_user('Please verify your email address', body_txt, 
                    html_message=body_html, fail_silently=False)


def verify_email(request, code):
    """Check for an email verification code in the querystring
    """

    session_code = request.session.get('verification_code', None)
    user_id = request.session.get('user_id', None)
    
    if session_code is None or user_id is None: 
        raise Http404()
    
    del request.session['verification_code']
    del request.session['user_id']
    
    print "        code is", code
    print "session_code is", session_code
    print "user id is", user_id
    print "request user is", request.user

    if code == session_code: 
        user = get_object_or_404(User, id=user_id)
        user.is_active = True
        user.save()

        return render(request, 'accounts/verify_email_success.html')
    else: 
        raise Http404()


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

        

