from social.exceptions import AuthException
from django.contrib.auth.models import Group
from django.http.response import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.conf import settings
from social.pipeline.partial import partial
import urlparse
import urllib
from django.shortcuts import redirect
from actions import apply_user_permissions
from django.core.context_processors import request


def get_social_details(user, backend, response, details, strategy, *args, **kwargs):
    """Create the UserData table, and gather data from the social provider and
    store it in the user data.
    Right now, we're just extracting the profile picture

    @type strategy social.strategies.django_strategy.DjangoStrategy
    """
    # from django.contrib.auth.models import User
    #
    # if not user:
    #     emails = []
    #     for email_record in response['emails']:
    #         emails.append(email_record['value'])
    #     emails = list(set(emails))
    #     user_candidates = User.objects.filter(email__in=emails)
    #     if user_candidates.count() == 0:
    #         user = User.objects.create(email=emails[0])
    #     elif user_candidates.count() == 1:
    #         user = user_candidates[0]
    #     else:
    #         # RDH Punt 09/12/2018
    #         user = user_candidates[0]
    #
    # import ipdb; ipdb.set_trace()

    # Handle backend-specific data collection, such as profile picture
    if backend.name == 'facebook':
        facebook_image_url = 'http://graph.facebook.com/v2.2/{id}/picture'
        # append ?redirect=false to get a result in JSON
        id = response.get('id', None)
        if id:
            user.userdata.profile_image = facebook_image_url.format(id=id)

    elif backend.name == 'google' or backend.name == 'google-oauth2':
        url_record = response.get('image', {})
        url_record = url_record.get('url')
        if url_record:
            # The default URL provides an image of size 50, we want size 64
            # so swap out ?sz=50 with ?sz=64
            url_record = urlparse.urlsplit(url_record)
            query = urllib.urlencode({'sz': '64'})
            # reassemble
            url_record = (url_record.scheme, url_record.netloc, url_record.path, query, url_record.fragment)
            url_record = urlparse.urlunsplit(url_record)

            user.userdata.profile_image = url_record

    elif backend.name == 'twitter':
        url_record = response.get('profile_image_url_https', '')
        if url_record:
            user.userdata.profile_image = url_record

    # If this is a new account, set the user's real & preferred names.
    if strategy.session_get('new_account'):
        user.userdata.real_name = details.get('real_name', '')
        user.userdata.preferred_name = details.get('preferred_name', '')

        # check to see if we have a trusted email address
        if details.get('unverified-email', True):
            user.userdata.email_verified = False
        else:
            user.userdata.email_verified = True

    user.userdata.save()

def set_user_permissions(strategy, details, user=None, *args, **kwargs):
    """Configure any initial permissions/groups for the user.
    """

    apply_user_permissions(user)


@partial
def confirm_account(strategy, details, user=None, is_new=False, *args, **kwargs):
    # If this is a new account, make sure the user sees the confirmation screen.
    # This allows them to enter/confirm their email address and name before they
    # continue to the site.
    # Every user gets to see this now.
    if is_new:
        strategy.session_set('new_account', True)

        if not strategy.session_get('seen-account-confirmation'):
            strategy.session_set('seen-account-confirmation', True)
            return redirect(reverse('account:social_confirm'))
    else:
        strategy.session_set('new_account', False)


def clean_session(strategy=None, *args, **kwargs):
    """If a user abandons the login in the middle, then various session
    variables may hang around and screw up the logic for the next try.
    This function cleans the session at the start of the pipeline and at the
    end.
    """

    strategy.session_pop('seen-account-confirmation')
