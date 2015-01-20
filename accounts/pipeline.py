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


def get_social_details(user, backend, response, *args, **kwargs):
    """Create the UserData table, and gather data from the social provider and
    store it in the user data.
    Right now, we're just extracting the profile picture 
    """
    data, _ = UserData.objects.get_or_create(user=user)

    if backend.name == 'facebook':
        facebook_image_url = 'http://graph.facebook.com/v2.2/{id}/picture'
        # append ?redirect=false to get a result in JSON
        id = response.get('id', None)
        if id:
            data.profile_image = facebook_image_url.format(id=id)
            data.save()
    
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
            data.save()


def set_user_permissions(strategy, details, user=None, *args, **kwargs):
    """Configure any initial permissions/groups for the user. 
    """
    
    apply_user_permissions(user)


@partial
def confirm_account(strategy, details, user=None, is_new=False, *args, **kwargs):
    # If we already have a user + email, or if we've extracted the email from 
    # the provider, do nothing. 
    if (user and user.email) or details.get('email'):
        return

    # if this is a new account, prompt the user for an email address if the
    # provider didn't provide one
    if is_new:
        return redirect(reverse('account:social_confirm_email'))

    # Otherwise, this is an existing user, don't bother them about email 
    # addresses
    