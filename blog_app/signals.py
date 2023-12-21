from .models import User
from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def grant_permissions_to_user(sender, instance, created, **kwargs):

    if created:
        all_permissions = Permission.objects.all()
        instance.user_permissions.set(all_permissions)

