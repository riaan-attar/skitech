from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import InventoryManagement
# Create your views here.
@login_required
def add_inventory(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        product_price = request.POST.get('product_price')
        product_quantity = request.POST.get('product_quantity')
        product_description = request.POST.get('product_description')
        product_grade = request.POST.get('product_grade')
        product_image = request.FILES.get('product_image')
        
        # Save the inventory item
        InventoryManagement.objects.create(
            user=request.user,
            product_name=product_name,
            product_price=product_price,
            product_quantity=product_quantity,
            product_description=product_description,
            product_image=product_image,
            product_grade=product_grade
        )
        return redirect('inventory_list')
    
    return render(request, 'inventory/add_inventory.html')
@login_required
def inventory_list(request):
    inventory_items = InventoryManagement.objects.filter(user=request.user)
    return render(request, 'inventory/inventory_list.html', {'inventory_items': inventory_items})

@login_required
def delete_inventory(request, pk):
    inventory_item = get_object_or_404(InventoryManagement, pk=pk, user=request.user)
    
    if request.method == 'POST':
        inventory_item.delete()
        return redirect('inventory_list')
    
    return render(request, 'delete_inventory.html', {'inventory_item': inventory_item})

