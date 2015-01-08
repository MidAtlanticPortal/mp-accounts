from social.exceptions import AuthException
from django.contrib.auth.models import Group
from django.http.response import HttpResponseRedirect

def user_password(strategy, user, is_new=False, *args, **kwargs):
    if strategy.backend.name != 'email': 
        return
       
    password = strategy.request_data()['password']
    if is_new: 
        user.set_password(password)
        user.save()
    
    elif not user.validate_password(password):
        raise AuthException(strategy.backend)

def save_redirect(strategy=None, *args, **kwargs):
    print "Welcome to save_redirect, kwargs are:", str(kwargs)
    return {'redirect_to': strategy.request.path}

def add_groups(strategy, details, user=None, *args, **kwargs):
    if not user or user.is_anonymous():
        return

    # test
    g, created = Group.objects.get_or_create(name='Designers')
    user.groups.add(g)

def redirect(redirect_to=None, *args, **kwargs):
    if redirect_to:
        print "**** Redirecting to", redirect_to
#         return HttpResponseRedirect('/account/user-info')
    