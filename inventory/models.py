from django.db import models

from user.models import CustomUser
class InventoryManagment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inventory_items')
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = models.IntegerField()
    product_description = models.TextField(null = True , blank = True)   
    product_image = models.ImageField(upload_to='static/assets/img',null = True)
    product_grade = models.CharField(max_length=100)
