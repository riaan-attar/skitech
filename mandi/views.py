from django.shortcuts import render

# Create your views here.
import requests
from django.shortcuts import render
from django.http import HttpResponse
import dotenv
import os

dotenv.load_dotenv()
def msp(request):
    # Default filter values
    filter_state = request.GET.get('state', 'Haryana')
    filter_district = request.GET.get('district', 'Gurgaon')
    filter_market = request.GET.get('market', 'Gurgaon')
    filter_commodity = request.GET.get('commodity', 'Pomegranate')

    # Base API URL
    base_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
    api_key=os.getenv('api_key1')

    # Constructing the data URL without variety and grade filters
    data_url = f"{base_url}?api-key={api_key}&format=json&filters%5Bstate.keyword%5D={filter_state}&filters%5Bdistrict%5D={filter_district}&filters%5Bmarket%5D={filter_market}&filters%5Bcommodity%5D={filter_commodity}"

    # Get the data using requests
    response = requests.get(data_url)

    # Check if the request was successful
    if response.status_code == 200:
        rawdata = response.json()
        records = rawdata.get('records', [])
        
        # Prepare data for rendering in the template
        context = {
            'records': records,
            'record_count': len(records),
            'filter_state': filter_state,
            'filter_district': filter_district,
            'filter_market': filter_market,
            'filter_commodity': filter_commodity,
        }
        return render(request, 'msp.html', context)
    else:
        return HttpResponse("Error fetching data")