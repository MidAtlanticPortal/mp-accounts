from django.db import models
# User = get_user_model()
from django.contrib.auth.models import User
import uuid

class EmailVerification(models.Model):
    """Model to store email address verification data. 
    """
    user = models.ForeignKey(User, unique=True) # one verification at a time
    email_to_verify = models.EmailField()
    verification_code = models.CharField(max_length=32, editable=False)
    # Expire verifications after XX days? 
    created = models.DateTimeField(auto_now_add=True)
    activate_user = models.BooleanField(default=True, 
        help_text=("If true, user.is_active will be set to true when verified."))

    def save(self, *args, **kwargs):
        self.verification_code = uuid.uuid4().hex
        return super(EmailVerification, self).save(*args, **kwargs)


class UserData(models.Model):
    """Model to store additional user-related information. 
    """
    user = models.OneToOneField(User, primary_key=True)
    email_verified = models.BooleanField(default=False, 
                                         help_text=("Has this user's email " 
                                                    "been verified?"))
#     avatar = models.URLField()
    
    