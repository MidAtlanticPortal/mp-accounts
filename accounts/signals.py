from accounts.models import UserData
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

@receiver(post_save, sender=User)
def user_post_save(instance, created, **kwargs):
    if created:
        data, new = UserData.objects.get_or_create(user=instance)

