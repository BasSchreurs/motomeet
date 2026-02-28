#meetings/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

def validate_image_size(image):
    max_size = 2 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Maximaal 2MB.")

class Meetup(models.Model):
    title = models.CharField("Titel", max_length=200)
    start_date = models.DateTimeField("Datum & tijd")
    end_date = models.DateTimeField("Eind datum & tijd", null=True, blank=True)
    location = models.CharField("Locatie", max_length=200)
    description = models.TextField("Beschrijving", blank=True)
    slug = models.SlugField("Slug", max_length=200, unique=True)
    image = models.ImageField("Afbeelding (bijv. screenshot van de route)", upload_to='meetups/', blank=True, null=True, validators=[validate_image_size])
    created_at = models.DateTimeField(auto_now_add=True)
    route_link = models.URLField("Route link", blank=True, null=True)
    document_link = models.URLField("Document link", blank=True, null=True)

    attendees = models.ManyToManyField(
        User,
        related_name='meetups_attending',
        blank=True,
        verbose_name="Deelnemers"
    )

    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='created_meetups',
        verbose_name="Aangemaakt door"
    )

    # NEW FIELDS for public/private functionality
    is_public = models.BooleanField(
        "Publieke meetup",
        default=True,
        help_text="Publieke meetups zijn zichtbaar voor iedereen. Private meetups zijn alleen voor uitgenodigde vrienden."
    )
    
    invited_friends = models.ManyToManyField(
        User,
        related_name='invited_to_meetups',
        blank=True,
        verbose_name="Uitgenodigde vrienden",
        help_text="Vrienden uitgenodigd voor deze private meetup"
    )

    class Meta:
        ordering = ['-start_date']
        verbose_name = "Meet-up"
        verbose_name_plural = "Meet-ups"

    def __str__(self):
        return self.title


class Comment(models.Model):
    meetup = models.ForeignKey(Meetup, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='meetup_comments')
    body = models.TextField("Reactie")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']
        verbose_name = "Reactie"
        verbose_name_plural = "Reacties"

    def __str__(self):
        return f"{self.author.username} op {self.meetup.title}"