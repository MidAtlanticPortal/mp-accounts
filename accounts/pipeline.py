from social.exceptions import AuthException
from django.contrib.auth.models import Group
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from social.pipeline.partial import partial
from models import UserData
import urlparse
import urllib
from django.shortcuts import redirect
from actions import apply_user_permissions
from django.core.context_processors import request


def get_social_details(user, backend, response, strategy, *args, **kwargs):
    """Create the UserData table, and gather data from the social provider and
    store it in the user data.
    Right now, we're just extracting the profile picture 
    """
    data, created = UserData.objects.get_or_create(user=user)

    if backend.name == 'facebook':
        facebook_image_url = 'http://graph.facebook.com/v2.2/{id}/picture'
        # append ?redirect=false to get a result in JSON
        id = response.get('id', None)
        if id:
            data.profile_image = facebook_image_url.format(id=id)
    
    elif backend.name == 'google-plus':
        url = response.get('image', {})
        url = url.get('url')
        if url:
            # The default URL provides an image of size 50, we want size 64
            # so swap out ?sz=50 with ?sz=64 
            url = urlparse.urlsplit(url)
            query = urllib.urlencode({'sz': '64'}) 
            # reassemble
            url = (url.scheme, url.netloc, url.path, query, url.fragment)
            url = urlparse.urlunsplit(url)

            data.profile_image = url

    if created: 
        # Only set email verification flags if we're new. 
        if strategy.session_get('unverified-email'):
            data.email_verified = False
        else:
            data.email_verified = True

    data.save()

def set_user_permissions(strategy, details, user=None, *args, **kwargs):
    """Configure any initial permissions/groups for the user. 
    """
    
    apply_user_permissions(user)


@partial
def confirm_account(strategy, details, user=None, is_new=False, *args, **kwargs):
    # If we already have an email, then the provider gave it to us or the user
    # entered it. Do nothing. 
    if details.get('email'):
        return

    # if this is a new account, prompt the user for an email address, but only
    # if the provider didn't provide one; mark the address as unverified. 
    if is_new:
        strategy.session_set('unverified-email', True)
        return redirect(reverse('account:social_confirm_email'))

    # Otherwise, this is an existing user, don't bother them about email 
    # addresses
    