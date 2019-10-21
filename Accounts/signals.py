    # Introducing signals to auto create user profile whene get's registred 

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    UserProfile, User
)

    # Creating a method to fire once user is registred

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user= instance)

    # Saving the user and his profile 
@receiver(post_save, sender = User)
def save_profile_user(sender, instance, **kwargs):
    instance.profile_user.save()


