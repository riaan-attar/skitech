from django.shortcuts import render

# Create your views here.
def market(request):
    return render(request, 'marketplace.html')

def mandi(request):
    return render(request, 'mandi.html')
