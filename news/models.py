from django.db import models

# Create your models here.

class Headline(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=500)
    published_at = models.DateTimeField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title