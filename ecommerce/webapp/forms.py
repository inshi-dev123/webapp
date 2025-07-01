from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Seller,Buyer,Product

class Seller_register_form(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), max_length=100)
    vendor_code = forms.CharField(max_length=3)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',) 

   
    def save_seller(self,commit=True):
        user=super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Seller.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                vendor_code=self.cleaned_data['vendor_code'],
                is_authorised=False
            )
        return user 
    
class Buyer_register_form(UserCreationForm):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email = forms.EmailField()
    phone = forms.CharField(max_length=15)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), max_length=100)
    city = forms.CharField()
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',) 

   
    def save_buyer(self,commit=True):
        user=super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Buyer.objects.create(
                user=user,
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                city=self.cleaned_data['city'],
            )
        return user 
    

from django import forms
from .models import Product

class Add_Product_Form(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name_product', 'description', 'price', 'photo']
        widgets = {

            'name_product': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product name'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the product'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'}),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'form-control'}),
                
                }
