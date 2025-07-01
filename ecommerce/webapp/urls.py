from django.contrib import admin
from django.urls import path
from  django.conf import settings
from .import views

urlpatterns = [
    path('',views.home,name='home'),
    path('/reg_sell',views.register_seller_view,name='register_seller'),
    path('register/buyer/', views.register_buyer_view, name='register_buyer'),
    path('products/', views.products, name='product_list'),
    path('logout/', views.logout_us, name='logout'),
    path('seller/dashboard/', views.seller_dashboard_view, name='seller_dashboard'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/<int:cart_id>/',views.view_cart,name='view_cart')

] 
