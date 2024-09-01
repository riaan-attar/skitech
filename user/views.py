from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from .models import *
from django.contrib.auth.decorators import login_required
import os
from market.models import *
def landing(request):
    return render(request,'index.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['name']
        email = request.POST['email']
        phone_no = request.POST['phone_number']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']
        role = request.POST.get('role')
        if password1 != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            phone_number=phone_no,
            role=role,
            password=password1
        )
        login(request,user)
        return redirect('login_view')
    return render(request,'sign-up.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.role == CustomUser.FARMER:
                return redirect('dashboard')  # Redirect to farmer's dashboard
            elif user.role == CustomUser.VENDOR:
                return redirect('vendor_dashboard')  # Redirect to vendor's dashboard
        else:
            return render(request, 'sign-in.html', {'error': 'Invalid username or password'})

    return render(request, 'sign-in.html')

        
@login_required        
def logout_view(request):
    logout(request)
    return redirect('landing')

WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
def weather_view(request):
    context = {
        'weather_api_key': WEATHER_API_KEY,
    }
    return render(request, 'weather.html', context)

def vendor_dashboard(request):
    return render(request, 'vendordash.html')

def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def add_to_cart(request, item_id):
    market_item = Market.objects.get(id=item_id)
    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        market_item=market_item,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_list')

@login_required
def remove_from_cart(request, item_id):
    cart_item = Cart.objects.get(id=item_id, user=request.user)
    if cart_item:
        cart_item.delete()
    return redirect('cart_list')


@login_required
def cart_list(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'cart_list.html', {'cart_items': cart_items})

@login_required
def place_order(request):
    cart_items = Cart.objects.filter(user=request.user)
    if cart_items.exists():
        for item in cart_items:
            Order.objects.create(
                user=request.user,
                market_item=item.market_item,
                quantity=item.quantity
            )
        cart_items.delete()  
        return redirect('order_list')  
    return redirect('cart_list')  

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order_list.html', {'orders': orders})
