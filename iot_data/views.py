from django.shortcuts import render
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Iot_data
import json

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Validate received data
            required_fields = ['moisture', 'temperature', 'humidity', 'nitrogen', 'phosphorus', 'potassium', 'ph']
            if all(field in data for field in required_fields):
                Iot_data.objects.create(
                    user=request.user,
                    moisture=data['moisture'],
                    temperature=data['temperature'],
                    humidity=data['humidity'],
                    nitrogen=data['nitrogen'],
                    phosphorus=data['phosphorus'],
                    potassium=data['potassium'],
                    ph=data['ph']  # Store the pH value
                )
                return JsonResponse({'status': 'success'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Invalid data structure'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'invalid request'}, status=400)



def display_data(request):
    
    iot_data = Iot_data.objects.filter(user=request.user).order_by('-date')
    
    context = {
        'iot_data': iot_data
    }
    
    return render(request, 'display_data.html', context)
