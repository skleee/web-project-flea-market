from django.contrib import admin
from .models import Product, Wish, Shoppinglist, Bid, Review

# Register your models here.
admin.site.register(Product)
admin.site.register(Wish)
admin.site.register(Shoppinglist)
admin.site.register(Bid)
admin.site.register(Review)