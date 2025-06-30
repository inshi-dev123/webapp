from django.contrib import admin
from .models import Seller,Product,Cart,Buyer

admin.site.register(Buyer)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(Seller)

# Register your models here.
