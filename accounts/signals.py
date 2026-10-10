from django.db.models.signals import post_save
from .models import UserProfile, User


def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
post_save.connect(create_profile, User)

