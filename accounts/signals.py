from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profiel

@receiver(post_save, sender=User)
def create_profiel(sender, instance, created, **kwargs):
    if created:
        Profiel.objects.get_or_create(
            gebruikersnaam=instance,
            defaults={"geboortedatum": None, "woonplaats": "", "motor_model": ""}
        )