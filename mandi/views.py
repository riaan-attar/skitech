from django.shortcuts import render
import requests
import os
import dotenv
from django.http import HttpResponse

dotenv.load_dotenv()

import os
import requests
from django.shortcuts import render
from django.http import HttpResponse

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
        state = request.POST.get('state', '').strip()
        district = request.POST.get('district', '').strip()
        market = request.POST.get('mandi', '').strip()
        commodity = request.POST.get('commodity', '').strip()

        # Validate inputs
        if not all([state, district, market,commodity]):
            return HttpResponse("All filter fields are required.")

        # Base API URL
        base_url = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
        api_key = os.getenv('api_key1')

        if not api_key:
            return HttpResponse("API key is missing.")

        # Constructing the data URL without variety and grade filters
        data_url = (
                    f"https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"
                    f"?api-key=579b464db66ec23bdd0000015a485d4cfa2e412d645f3021958e7456"
                    f"&format=json"
                    f"&filters%5Bstate.keyword%5D={state}"
                    f"&filters%5Bdistrict%5D={district}"
                    f"&filters%5Bmarket%5D={market}"
                    f"&filters%5Bcommodity%5D={commodity}"
                    )
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
                'filter_state': state,
                'filter_district': district,
                'filter_market': market,
                'filter_commodity': commodity,
            })

        except requests.exceptions.RequestException as e:
            # Log the error or print it
            print(f"Error fetching data: {e}")
            return HttpResponse("Error fetching data")

    # Render the template with the context
    return render(request, 'mandi.html', context)
