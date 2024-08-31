from django.shortcuts import render

# Create your views here.
# news/views.py

from django.shortcuts import render
from .models import Headline

def headlines_list(request):
    headlines = Headline.objects.all().order_by('-published_at')
    context = {'headlines': headlines}
    return render(request, 'news/headlines.html', context)
