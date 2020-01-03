from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from accounts.models import Buyer, Seller

# Create your models here.
class Product(models.Model):
    TYPES = [
        ('AC', 'Auction'),
        ('FL', 'Flea Market'),
    ]
    STATUS=[
       ('AUC', 'Auction'),
       ('PUR', 'Purchased'),
       ('ING', 'In Progress'),
    ]
    status = models.CharField(
        max_length=3,
        choices = STATUS,
        default = 'ING',
    )
    type = models.CharField(
        max_length = 2,
        choices = TYPES,
        default = 'FL'
    )
    pid = models.IntegerField(primary_key=True) #pk
    sellid = models.ForeignKey(User,on_delete=models.CASCADE, null=True, blank=True) #seller
    pimg = models.ImageField(blank=True) #image
    category = models.CharField(max_length=20) #category
    price = models.IntegerField() #price
    pname = models.CharField(max_length=20) #product name
    stock = models.IntegerField(default = 0) #stock remaining
    pub_date = models.DateField('product registered', default = timezone.now) #registered date
    tradeplace = models.CharField(max_length=30, default='Seoul') #trading place
    #If Auction
    endtime = models.DateField('auction ended', default = timezone.now, null=True) #auction end time   
    def __str__(self):
        return self.pname

class Bid(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.IntegerField(default = 0) #Bid price
    bidtime = models.DateField('bid made', default = timezone.now)
    def __str__(self):
        return "User ID: " + str(self.uid) + " Product ID: " + str(self.pid) + " at " + str(self.bidtime)

class Shoppinglist(models.Model):
    pid = models.ForeignKey(Product, on_delete = models.CASCADE)
    uid = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.uid) + "," + str(self.pid)

class Wish(models.Model):
    pid = models.ForeignKey(Product, on_delete = models.CASCADE)
    uid = models.ForeignKey(User, on_delete = models.CASCADE)
    def __str__(self):
        return str(self.uid) + "," + str(self.pid)

class Review(models.Model):
    uid = models.ForeignKey(User, on_delete= models.CASCADE)
    pid = models.ForeignKey(Product, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    pubdate = models.DateField('review made', default = timezone.now)
    def __str__(self):
        return str(self.uid) + "'s review for" + str(self.pid)