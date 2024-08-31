from django.db import models
from django.db import models

class Headline(models.Model):
    headline = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.headline
