from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime

# Create your models here.
class Topping(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5, decimal_places=2)  # Price for the topping

    def __str__(self):
        return self.name
    
class Product(models.Model):
    CATEGORY_CHOICES = [
        ('classic', 'Classic'),
        ('special', 'Special Order'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    price_1kg= models.DecimalField(max_digits=10, decimal_places=2)
    price_1_5kg= models.DecimalField(max_digits=10, decimal_places=2)
    price_2kg= models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)        
    toppings = models.ManyToManyField(Topping, related_name='product', blank=True)  # Ensure toppings is ManyToManyField


    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cake_size_kg = models.DecimalField(max_digits=5, decimal_places=2)
    occasion = models.CharField(max_length=100)
    preferred_colors = models.CharField(max_length=200)
    toppings = models.CharField(max_length=200)
    delivery_date = models.DateTimeField()
    #delivery_time = models.TimeField()
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_high_urgency(self):
        return self.delivery_date <= datetime.now() + timedelta(hours=24)
