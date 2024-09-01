from django.shortcuts import render
import requests
import os
import dotenv
from django.http import HttpResponse

dotenv.load_dotenv()

def mandi(request):
    # Default context if no POST request is made
    context = {
        'records': [],
        'record_count': 0,
        'filter_state': '',
        'filter_district': '',
        'filter_market': '',
        'filter_commodity': '',
    }

    # Check if the request is a POST request
    if request.method == 'POST':
        # Get the filter values from the POST data
        filter_state = request.POST.get('state')
        filter_district = request.POST.get('district')
        filter_market = request.POST.get('mandi')
        filter_commodity = request.POST.get('commodity')

        # Base API URL
        base_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        api_key = os.getenv('MANDI_API_KEY')

        # Constructing the data URL without variety and grade filters
        data_url = f"{base_url}?api-key={api_key}&format=json&filters%5Bstate.keyword%5D={filter_state}&filters%5Bdistrict%5D={filter_district}&filters%5Bmarket%5D={filter_market}&filters%5Bcommodity%5D={filter_commodity}"

        # Get the data using requests
        try:
            response = requests.get(data_url)
            response.raise_for_status()  # Raise an error for bad status codes
            rawdata = response.json()
            records = rawdata.get('records', [])

            # Prepare data for rendering in the template
            context.update({
                'records': records,
                'record_count': len(records),
                'filter_state': filter_state,
                'filter_district': filter_district,
                'filter_market': filter_market,
                'filter_commodity': filter_commodity,
            })

        except requests.exceptions.RequestException as e:
            # Log the error or print it
            print(f"Error fetching data: {e}")
            return HttpResponse("Error fetching data")

    # Render the template with the context
    return render(request, 'mandi.html', context)
