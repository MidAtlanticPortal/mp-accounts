from django.conf import settings

def login_disabled(request):
    """Facility for disabling site logins and registrations. Provides the 
    LOGIN_DISABLED context variable for use in templates.
    
    Currently, logins are only enabled in DEBUG configurations.  
    """
    
    return dict(LOGIN_DISABLED=not settings.DEBUG)
