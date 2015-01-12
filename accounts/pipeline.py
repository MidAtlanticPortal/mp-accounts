from social.exceptions import AuthException
from django.contrib.auth.models import Group
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from social.pipeline.partial import partial

@partial
def require_email(strategy, backend, details, user=None, is_new=False, 
                  **kwargs):
    """Make sure that all users come with an email address.
    """
    
    if user and user.email:
        # Force validation of new email address
        if backend.name == 'email':
            return {'is_new': True}

        return

    elif is_new and not details.get('email'):
        if strategy.session_get('saved_email'):
            details['email'] = strategy.session_pop('saved_email')
        else:
            return redirect('register')
 

def send_validation_email(strategy, backend, code):
    print "*** In validate_email"
    print code.code
    print code.email
    print code.verified
    
    link = strategy.build_absolute_uri(reverse('social:complete', 
                                               args=(backend.name,)))
    link += '?verification_code=%s' % code.code

    print link
    
    # TODO: Move this to template
    message_body = '''
    Hi, someone gave this email address while signing up for an account on 
    http://midatlanticocean.org. If it wasn't you, then please discard this email. 
    
    Otherwise, click on this link to validate your email address and complete
    the sign in process:
    
        %s
    
    Regards, 
    
    The MARCO Portal Team
    ''' % link
    
    send_mail('Please validate your email address', message_body, 
              settings.DEFAULT_FROM_EMAIL, [code.email], fail_silently=False)
    
def user_password(strategy, user, backend=None, is_new=False, *args, **kwargs):
    if backend.name != 'email': 
        return
       
    password = strategy.request_data()['password']
    if is_new: 
        user.set_password(password)
        user.save()
    
    elif not user.check_password(password):
        raise AuthException(strategy.backend)


def save_redirect(strategy=None, *args, **kwargs):
    print "Welcome to save_redirect, kwargs are:", str(kwargs)
    return {'redirect_to': strategy.request.path}


def set_user_permissions(strategy, details, user=None, *args, **kwargs):
    """Configure any initial permissions/groups for the user. 
    """
    if not user or user.is_anonymous():
        return

    # test
    g, created = Group.objects.get_or_create(name='Designers')
    user.groups.add(g)
    
    # Automatically promote @pointnineseven.com users to admins
    if settings.DEBUG:
        email = user.email
        email = email.split('@')
        if len(email) == 2 and email[1] == 'pointnineseven.com': 
            user.is_staff = True
            user.is_superuser = True
            user.save()


def redirect(redirect_to=None, *args, **kwargs):
    if redirect_to:
        print "**** Redirecting to", redirect_to
#         return HttpResponseRedirect('/account/user-info')
    