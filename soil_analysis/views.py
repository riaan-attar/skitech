from django.shortcuts import render
from soil_analysis.utils import *
from django.shortcuts import render
import os
from django.shortcuts import render, redirect, HttpResponse
import pdfplumber as pp
import google.generativeai as genai
import numpy as np
import pickle
import dotenv
from django.http import JsonResponse
from sklearn.ensemble import RandomForestClassifier 
import base64
from io import BytesIO
from django.core.files.base import ContentFile 
dotenv.load_dotenv()

def disease_info(request):
    if request.method == 'POST':
        if 'image' in request.FILES:
            uploaded_file = request.FILES['image']
            image_base64 = get_base64_image(uploaded_file)
            temp_dir = 'temp'
            image_path = None  # Initialize image_path
            
            try:
                if not os.path.exists(temp_dir):
                    os.makedirs(temp_dir)
                image_path = os.path.join(temp_dir, uploaded_file.name)
                
                with open(image_path, 'wb+') as destination:
                    for chunk in uploaded_file.chunks():
                        destination.write(chunk)
                
                # Predict plant name and disease
                plant_name, disease = predict_image(image_path)
                plant_name = plant_name.replace('_', ' ')
                disease = disease.replace('_', ' ')
                
                # Define API key
                api_key = os.getenv("GOOGLE_API_KEY")
                
                # Create prompts for each section
                prompts = {
                    "description": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Provide a detailed description of the disease called {disease} affecting the {plant_name} plant, strictly avoid use of special characters such as \\n or ##.",
                    "causes": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Provide detailed information about the causes of the disease called {disease} affecting the {plant_name} plant, strictly avoid use of special characters such as \\n or ##.",
                    "prevention": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Provide detailed prevention methods for the disease called {disease} affecting the {plant_name} plant, strictly avoid use of special characters such as \\n or ##.",
                    "best_practices": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Provide the best practices to manage the disease called {disease} affecting the {plant_name} plant, strictly avoid use of special characters such as \\n or ##.",
                    "fertilizers": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Recommend fertilizers for the disease called {disease} affecting the {plant_name} plant, strictly avoid use of special characters such as \\n or ##.",
                    "pesticides": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Recommend pesticides for the disease called {disease} affecting the {plant_name} plant, strictly avoid use of special characters such as \\n or ##."
                }
                
                # Fetch content for each section
                description = generate_content(prompts["description"], api_key)
                causes = generate_content(prompts["causes"], api_key)
                prevention = generate_content(prompts["prevention"], api_key)
                best_practices = generate_content(prompts["best_practices"], api_key)
                fertilizers = generate_content(prompts["fertilizers"], api_key)
                pesticides = generate_content(prompts["pesticides"], api_key)
                
                # Prepare context for the response
                context = {
                    'plant_name': plant_name,
                    'disease': disease,
                    'description': format_generated_text(description),
                    'causes': format_generated_text(causes),
                    'prevention': format_generated_text(prevention),
                    'best_practices': format_generated_text(best_practices),
                    'fertilizers': format_generated_text(fertilizers),
                    'pesticides': format_generated_text(pesticides),
                    'image_base64': image_base64
                }
                return render(request, 'diseases.html', context)
            
            except Exception as e:
                # Handle exceptions and render an error page
                return render(request, 'diseases.html', {'error': str(e)})
            
            finally:
                # Cleanup temp file
                if image_path and os.path.exists(image_path):
                    os.remove(image_path)
        
    return render(request, 'diseases.html')
# Create your views here.

def crop_recommendation(request):
    # Define the path to the model
    model_path = 'soil_analysis/Random_Forest_model.pkl'
    
    # Check if the model file exists and load it
    if os.path.exists(model_path):
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
    else:
        return HttpResponse(f"Model file not found at {model_path}", status=404)
    
    if request.method == 'POST':
        
        nitrogen = float(request.POST.get('nitrogen', 0))
        phosphorus = float(request.POST.get('phosphorus', 0))
        potassium = float(request.POST.get('potassium', 0))
        temperature = float(request.POST.get('temperature', 0))
        humidity = float(request.POST.get('humidity', 0))
        ph = float(request.POST.get('ph', 0))
        rainfall = float(request.POST.get('rainfall', 0))
        
        features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])
    
        try:
            predicted_crop = model.predict(features)[0]
            
            # Prepare the prompts
            prompts = {
                "fertilizer": (
                    f"assume you are an expert in all things related to agriculture and you have been asked to recommend "
                    f"fertilizer type for a crop {predicted_crop} for soil having nitrogen {nitrogen}kg/ha, "
                    f"phosphorus {phosphorus}kg/ha, potassium {potassium}kg/ha, and pH {ph} in a region where "
                    f"humidity is {humidity}% and rainfall is {rainfall}mm. Return the response in less than one hundred "
                    f"words without using special characters."
                ),
                "best_practice": (
                    f"assume you are an expert in all things related to agriculture and you have been asked to recommend "
                    f"best practices for growing crop {predicted_crop} in soil with nitrogen {nitrogen}kg/ha, "
                    f"phosphorus {phosphorus}kg/ha, potassium {potassium}kg/ha, and pH {ph}. The region has "
                    f"humidity of {humidity}% and rainfall of {rainfall}mm. Return the response in less than one hundred "
                    f"words without using special characters."
                )
            }

            api_key = os.getenv("GOOGLE_API_KEY")
            image_url = f'static/crop_images/{predicted_crop}.jpg'
            image_base64 = base64_image(image_url)
            # Call the generate_content function for each prompt
            fert = generate_content(prompts["fertilizer"], api_key)
            best_ = generate_content(prompts["best_practice"], api_key)
            
            # Format the generated text
            fertilizer = format_generated_text(fert)
            best_practice = format_generated_text(best_)
            
            # Prepare the context
            context = {
                'predicted_crop': predicted_crop,
                'image': image_base64,
                'fertilizer': fertilizer,
                'best_practice': best_practice,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            }

        except Exception as e:
            return HttpResponse(f"Error making prediction: {str(e)}", status=500)     
        return render(request, 'croprecom.html', context)
    return render(request, 'crop_recommendation_form.html')

def soil_analysis(request):
    if request.method == 'POST':
        # Handle the uploaded PDF file
        uploaded_file = request.FILES['soil_report']
        temp_dir = 'temp'
        pdf_path = os.path.join(temp_dir, uploaded_file.name)
        
        # Save the uploaded PDF file
        with open(pdf_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        # Extract text from the PDF
        try:
            soil_report_text = extract_text_from_pdf(pdf_path)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        api_key = os.getenv("GOOGLE_API_KEY")
        try:
            # Configure the API client
            genai.configure(api_key=api_key)
            
            # Initialize the GenerativeModel
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Generate content using the model
            response = model.generate_content(
                f"Assume you are an expert in soil science and you have been asked to analyze the following soil report: {soil_report_text}. "
                f"Provide a detailed analysis and recommendations for improving soil health based on the provided report. "
                f"Return the text in a human understandable language, suitable for a farmer, without any special characters such as # /n or ** in the response."
            )
            
            # Extract the generated text from the response
            candidates = getattr(response, 'candidates', [])
            if candidates:
                candidate = candidates[0]
                content = getattr(candidate, 'content', {})
                parts = getattr(content, 'parts', [])
                if parts:
                    generated_text = parts[0].text
                else:
                    generated_text = 'No text parts found in the response'
            else:
                generated_text = 'No candidates found in the response'
            
            # Prepare context for the response
            context = {
                'generated_text': generated_text,
                'soil_report_text': soil_report_text
            }
            return render(request, 'pdf.html', context)
        
        except Exception as e:
            return render(request, 'pdf.html', {'error': str(e)})
        
        finally:
            # Cleanup temp file
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
    
    return render(request, 'pdf.html')


