from django.db.models.base import post_save
from django.dispatch import receiver
from django.signals import Signal

from .models import UserProfile


@receiver(post_save, sender=)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
