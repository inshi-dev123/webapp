from django.db import models
from django.contrib.auth.models import User

class Buyer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address =  models.CharField(max_length=40)
    city =  models.CharField(max_length=50)

    def __str__(self):
        return self.user.username
    
class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address=models.TextField(max_length=50)
    phone = models.CharField(max_length=15)
    vendor_code=models.CharField(max_length=3)
    is_authorised=models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username

class Product(models.Model):
    name_product=models.CharField(max_length=30) #name
    description=models.TextField(max_length=50) #descript
    price=models.FloatField() #get price
    photo=models.ImageField(upload_to='photo/',blank=True , null=True) #a pic of product
    seller_pr=models.ForeignKey(Seller,on_delete=models.CASCADE) #link to seller
    created_at=models.DateTimeField(auto_now_add=True) #timestamp for adding product

    def __str__(self):
        return self.name_product



class Cart(models.Model):
    user_buyer=models.OneToOneField(Buyer,on_delete=models.CASCADE) #each cart can have buyer only atm 
    items=models.ManyToManyField(Product) # get multiple products in one cart for one buyer only 

    def __str__(self):
        return self.user_buyer.user.username


