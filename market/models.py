from django.db import models

# Create your models here.
class Market(models.Model):
    user = models.ForeignKey('user.CustomUser', on_delete=models.CASCADE, related_name='market_item')
    title = models.CharField(max_length=250)
    price = models.IntegerField(blank=True)
    image = models.FileField(upload_to='static/assets/img')
    description = models.TextField()
    phone = models.CharField(max_length=15)
