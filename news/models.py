from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)               # Article title
    content = models.TextField()                           # Full content
    published_at = models.DateTimeField(auto_now_add=True) # Auto timestamp
    slug = models.SlugField(max_length=200, unique=True)  # URL-friendly name
    image = models.ImageField(upload_to='articles/', blank=True, null=True)

    class Meta:
        ordering = ['-published_at']  # newest first

    def __str__(self):
        return self.title