from django.shortcuts import render,redirect,get_object_or_404
from .forms import Seller_register_form, Buyer_register_form, Add_Product_Form
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product,Seller,Buyer,Cart
from django.core.paginator import Paginator
# Create your views here.
def home(request):
    products = Product.objects.all()
    cart = None

    if request.user.is_authenticated:
        try:
            buyer = Buyer.objects.get(user=request.user)
            cart = Cart.objects.filter(user_buyer=buyer).first()
        except Buyer.DoesNotExist:
            cart = None

    if request.method == 'POST':
        username = request.POST['User_name']
        passwd = request.POST['Password']
        user = authenticate(request, username=username, password=passwd)

        if user is not None:
            try:
                seller = Seller.objects.get(user=user)
                if not seller.is_authorised:
                    messages.error(request, "Your seller account is not authorized yet.")
                    return redirect('home')
                else:
                    login(request, user)
                    return redirect('seller_dashboard')
            except Seller.DoesNotExist:
                login(request, user)
                messages.success(request, "You have been logged in as a buyer")
                return redirect('product_list')
        else:
            messages.error(request, "Invalid credentials. Please try again.")

    return render(request, 'home.html', {'products': products, 'cart': cart})




def seller_dashboard_view(request):
    try:
        seller = Seller.objects.get(user=request.user)
        products = Product.objects.filter(seller_pr=seller)

        if request.method == 'POST':
            form = Add_Product_Form(request.POST, request.FILES)
            if form.is_valid():
                product = form.save(commit=False)
                product.seller_pr = seller
                product.save()
                messages.success(request, "Product added successfully.")
                return redirect('seller_dashboard')  # prevent resubmission
        else:
            form = Add_Product_Form()

        return render(request, 'seller_dashboard.html', {
            'products': products,
            'form': form
        })
    except Seller.DoesNotExist:
        messages.error(request, "You are not registered as a seller.")
        return redirect('home')


def register_seller_view(request):
    if request.method == 'POST':
        form = Seller_register_form(request.POST)
        if form.is_valid():
            form.save_seller()
            return redirect('home')  
    else:
        form = Seller_register_form()

    return render(request, 'register_seller.html', {'form': form})

def register_buyer_view(request):
    if request.method == 'POST':
        form = Buyer_register_form(request.POST)
        if form.is_valid():
            form.save_buyer()
            return redirect('home')  
    else:
        form = Buyer_register_form()

    return render(request, 'register_buyer.html', {'form': form})

def products(request):
    products = Product.objects.all()
    p = Paginator(products, 2)
    page = request.GET.get('page')
    product_list = p.get_page(page)

    cart = None
    if request.user.is_authenticated:
        try:
            buyer = Buyer.objects.get(user=request.user)
            cart = Cart.objects.filter(user_buyer=buyer).first()
        except Buyer.DoesNotExist:
            cart = None

    return render(request, 'buyer_dashboard.html', {
        'products': products,
        'product_list': product_list,
        'cart': cart
    })


def logout_us(request):
    logout(request)
    messages.success(request,"You have been successfully logged out ")
    return redirect('home')

def add_to_cart(request,product_id):
    prod=get_object_or_404(Product,id=product_id)
    buyer=get_object_or_404(Buyer,user=request.user)
    cart,create=Cart.objects.get_or_create(user_buyer=buyer)
    cart.items.add(prod)
    return redirect('product_list')

def view_cart(request, cart_id):
    cart = get_object_or_404(Cart, id=cart_id)
    items = cart.items.all()
    return render(request, 'cart.html', {'items': items})
