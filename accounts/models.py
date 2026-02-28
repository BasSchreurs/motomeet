from django.contrib.auth.models import User
from django.db import models
from datetime import date
from django.core.exceptions import ValidationError

def validate_image_size(image):
    max_size = 2 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Maximaal 2MB.")

class Profiel(models.Model):
    gebruikersnaam = models.OneToOneField(User, on_delete=models.CASCADE)
    profiel_foto = models.ImageField("Profielfoto", upload_to='profielen/', blank=True, null=True, validators=[validate_image_size],)
    geboortedatum = models.DateField(null=True, blank=True, verbose_name="Geboortedatum")
    woonplaats = models.CharField(max_length=100, blank=True, verbose_name="Woonplaats")
    motor_model = models.CharField(max_length=100, blank=True, verbose_name="Motor Model")

    # Social media
    instagram = models.URLField("Instagram", blank=True, null=True)
    facebook = models.URLField("Facebook", blank=True, null=True)
    whatsapp = models.URLField("WhatsApp", blank=True, null=True)
    youtube = models.URLField("YouTube", blank=True, null=True)
    tiktok = models.URLField("TikTok", blank=True, null=True)

    # Favourite routes
    route_1_naam = models.CharField("Route 1 naam", max_length=100, blank=True, null=True)
    route_1 = models.URLField("Route 1", blank=True, null=True)
    route_2_naam = models.CharField("Route 2 naam", max_length=100, blank=True, null=True)
    route_2 = models.URLField("Route 2", blank=True, null=True)
    route_3_naam = models.CharField("Route 3 naam", max_length=100, blank=True, null=True)
    route_3 = models.URLField("Route 3", blank=True, null=True)
    route_4_naam = models.CharField("Route 4 naam", max_length=100, blank=True, null=True)
    route_4 = models.URLField("Route 4", blank=True, null=True)
    route_5_naam = models.CharField("Route 5 naam", max_length=100, blank=True, null=True)
    route_5 = models.URLField("Route 5", blank=True, null=True)

    #vrienden
    vrienden = models.ManyToManyField(
        User,
        related_name="toegevoegd_door",
        blank=True
    )

    def is_complete(self):
        return all([
            self.geboortedatum,
            self.woonplaats,
            self.motor_model
        ])

    def __str__(self):
        return self.gebruikersnaam.username

    @property
    def leeftijd(self):
        today = date.today()
        born = self.geboortedatum
        if born:
            return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return None

    @property
    def sociale_media(self):
        """Returns a list of (platform, url, icon) tuples for any filled-in socials."""
        platforms = [
            ("Instagram", self.instagram, "fa-brands fa-instagram"),
            ("Facebook", self.facebook, "fa-brands fa-facebook"),
            ("WhatsApp", self.whatsapp, "fa-brands fa-whatsapp"),
            ("YouTube", self.youtube, "fa-brands fa-youtube"),
            ("TikTok", self.tiktok, "fa-brands fa-tiktok"),
        ]
        return [(name, url, icon) for name, url, icon in platforms if url]

    @property
    def favoriete_routes(self):
        routes = [
            (self.route_1_naam or "Route 1", self.route_1),
            (self.route_2_naam or "Route 2", self.route_2),
            (self.route_3_naam or "Route 3", self.route_3),
            (self.route_4_naam or "Route 4", self.route_4),
            (self.route_5_naam or "Route 5", self.route_5),
        ]
        return [(label, url) for label, url in routes if url]
        