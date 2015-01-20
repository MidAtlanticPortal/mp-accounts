from django.contrib.auth.models import Group
from django.conf import settings

def apply_user_permissions(user):
    """Configure any initial permissions/groups for the user. 
    """

    if not user or user.is_anonymous():
        return

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
