from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from .models import Market
from user.models import CustomUser, Order



@login_required
def add_market_item(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        price = request.POST.get('price')
        description = request.POST.get('description')
        phone = request.POST.get('phone')
        image = request.FILES.get('image')
        
        if title and price and description and phone and image:
            Market.objects.create(
                user=request.user,
                title=title,
                price=price,
                description=description,
                phone=phone,
                image=image
            )
            return redirect('market_list')  
    return render(request, 'add_market_item.html')


def market_list(request):
    items = Market.objects.all()
    return render(request, 'market_list.html', {'items': items})
@login_required
def vendor_orders(request):
    
    if request.user.role != 'vendor':
        return render(request, '403.html', status=403)
    
    
    orders = Order.objects.filter(user=request.user)
    

    return render(request, 'vendor_orders.html', {'orders': orders})

<<<<<<< HEAD
# Create your views here.
def market(request):
    return render(request, 'marketplace.html')

def mandi(request):
    return render(request, 'mandi.html')
=======
>>>>>>> f40bbd4ae679fec88f986f9431eedf9deedb78c0
