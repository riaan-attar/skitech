from django.db import models
from user.models import CustomUser
# Create your models here.
class Iot_data(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='iot_data')
    temperature = models.DecimalField(max_digits=10, decimal_places=2)
    humidity = models.DecimalField(max_digits=10, decimal_places=2)
    moisture = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    nitrogen = models.DecimalField(max_digits=10, decimal_places=2)
    phosphorus = models.DecimalField(max_digits=10, decimal_places=2)
    potassium = models.DecimalField(max_digits=10, decimal_places=2)
    ph = models.DecimalField(max_length = 10,decimal_places=2 )
