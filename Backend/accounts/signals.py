from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Language


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Profile)
def set_default_language(sender, instance, created, **kwargs):
    if created and instance.languages.count() == 0:
        english = Language.objects.filter(name="English").first()
        if english:
            instance.languages.add(english)