from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import authenticate,login,logout
from .models import CustomUser
from django.contrib.auth.decorators import login_required
import os
def landing(request):
    return render(request,'index.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
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
                return redirect('farmer_dashboard')  # Redirect to farmer's dashboard
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