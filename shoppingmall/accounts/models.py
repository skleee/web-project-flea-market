from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

#Buyer
class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE) #1:1 mapping with user model
    is_buyer = models.BooleanField(default = False) #True if buyer
    is_seller = models.BooleanField(default = False) #True if seller
    pids = models.ManyToManyField(to='shop.Product')  #M:N mapping with "Product" id
    address = models.TextField(max_length=100) #address
    
    def __str__(self):
        return self.user.username

#Seller
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)  #1:1 mapping with user model
    is_buyer = models.BooleanField(default = False) #True if buyer
    is_seller = models.BooleanField(default = False)#True if seller
    phone = models.IntegerField(default = 0) 
    def __str__(self):
        return self.user.username