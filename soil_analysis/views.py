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
import re
from django.http import JsonResponse
from sklearn.ensemble import RandomForestClassifier 
import base64
from io import BytesIO
from django.core.files.base import ContentFile
import numpy as np
from io import BytesIO
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

from django.template.loader import render_to_string
from django.conf import settings 
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

from django.shortcuts import render
import os
import pickle
import numpy as np
from django.http import HttpResponse
from soil_analysis.utils import base64_image, format_generated_text, generate_content

from django.shortcuts import render
import os
import pickle
import numpy as np
from django.http import HttpResponse
from soil_analysis.utils import base64_image, format_generated_text, generate_content

def crop_recommendation(request):
    model_path = 'soil_analysis/Random_Forest_model.pkl'

    if os.path.exists(model_path):
        with open(model_path, 'rb') as file:
            model = pickle.load(file)
    else:
        return HttpResponse(f"Model file not found at {model_path}", status=404)

    if request.method == 'POST':
        try:
            nitrogen = float(request.POST.get('nitrogen', 0))
            phosphorus = float(request.POST.get('phosphorus', 0))
            potassium = float(request.POST.get('potassium', 0))
            temperature = float(request.POST.get('temperature', 0))
            humidity = float(request.POST.get('humidity', 0))
            ph = float(request.POST.get('ph', 0))
            rainfall = float(request.POST.get('rainfall', 0))
            fcrop1 = request.POST.get('former_crop')
            fcrop2 = request.POST.get('former_crop2')
            fcrop3 = request.POST.get('former_crop3')
            past_practices = request.POST.get('description')
            # Constraints for the input values
            if not (0 <= nitrogen <= 300 and 0 <= phosphorus <= 300 and 0 <= potassium <= 300 and
                    0 <= temperature <= 60 and 0 <= humidity <= 100 and 0 <= ph <= 14 and
                    0 <= rainfall <= 2000):
                return HttpResponse("Invalid input values", status=400)

            features = np.array([[nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall]])

            # Get the top 3 predicted crops
            predicted_proba = model.predict_proba(features)[0]
            top_3_indices = np.argsort(predicted_proba)[-3:][::-1]
            top_3_crops = [model.classes_[i] for i in top_3_indices]

            # Store crop information in different variables
            crop_1, crop_2, crop_3 = top_3_crops[0], top_3_crops[1], top_3_crops[2]
            image_url_1 = f'static/crop_images/{crop_1}.jpg'
            image_url_2 = f'static/crop_images/{crop_2}.jpg'
            image_url_3 = f'static/crop_images/{crop_3}.jpg'
            request.session['best_crops'] = top_3_crops
            request.session['nitrogen'] = nitrogen
            request.session['phosphorus'] = phosphorus
            request.session['potassium'] = potassium
            request.session['temperature'] = temperature
            request.session['humidity'] = humidity
            request.session['ph'] = ph
            request.session['rainfall'] = rainfall
            request.session['fcrop1'] = fcrop1
            request.session['fcrop2'] = fcrop2
            request.session['fcrop3'] = fcrop3
            request.session['past_practices'] = past_practices

    
            
            prompts = {
                "maturation1": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Provide a rough maturation period of {crop_1} in one line, strictly avoid use of special characters such as \\n or ##.",
                "maturation2": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Provide a rough maturation period of {crop_2} in one line, strictly avoid use of special characters such as \\n or ##.",
                "maturation3": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Provide a rough maturation period of {crop_3} in one line, strictly avoid use of special characters such as \\n or ##.",
                "feasibility1": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Provide a brief feasibility analysis of {crop_1}in 3 to 4 sentences, strictly avoid use of special characters such as \\n or ##.",
                "feasibility2": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Provide a brief feasibility analysis of {crop_2}in 3 to 4 sentences, strictly avoid use of special characters such as \\n or ##.",
                "feasibility3": f"Assume you are an expert in Agriculture specializing in Indian agriculture. Provide a brief feasibility analysis of {crop_3}in 3 to 4 sentences, strictly avoid use of special characters such as \\n or ##.",
            }

            # Fetch content for each crop
            maturation_time_1 = generate_content(prompts["maturation1"], api_key)
            feasibility_1 = generate_content(prompts["feasibility1"], api_key)

            maturation_time_2 = generate_content(prompts["maturation2"], api_key)
            feasibility_2 = generate_content(prompts["feasibility2"], api_key)

            maturation_time_3 = generate_content(prompts["maturation3"], api_key)
            feasibility_3 = generate_content(prompts["feasibility3"], api_key)
            
            # Prepare crop information
            crop_info_1 = {
                'crop': crop_1,
                'image': base64_image(image_url_1),
                'maturation_time': format_generated_text(maturation_time_1),
                'feasibility': format_generated_text(feasibility_1),
            }

            crop_info_2 = {
                'crop': crop_2,
                'image': base64_image(image_url_2),
                'maturation_time': format_generated_text(maturation_time_2),
                'feasibility': format_generated_text(feasibility_2),
            }

            crop_info_3 = {
                'crop': crop_3,
                'image': base64_image(image_url_3),
                'maturation_time': format_generated_text(maturation_time_3),
                'feasibility': format_generated_text(feasibility_3),
            }

            context = {
                'crop_info_1': crop_info_1,
                'crop_info_2': crop_info_2,
                'crop_info_3': crop_info_3,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            }
            return render(request, 'croprecom.html', context)

        except ValueError:
            return HttpResponse("Invalid input format", status=400)
        except Exception as e:
            return HttpResponse(f"Error making prediction: {str(e)}", status=500)

    return render(request, 'crop_recommendation_form.html')


from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
from .utils import generate_content, api_key
from .utils import render_to_pdf  # Ensure this import matches your project structure

def work_plan(request):
    # Retrieve form data from session
    fcrop1 = request.session.get('fcrop1')
    fcrop2 = request.session.get('fcrop2')
    fcrop3 = request.session.get('fcrop3')
    past_practices = request.session.get('past_practices')
    
    # Retrieve session data
    crop_recommendations = request.session.get('best_crops', [])
    soil_data = {
        'nitrogen': request.session.get('nitrogen'),
        'phosphorus': request.session.get('phosphorus'),
        'potassium': request.session.get('potassium'),
        'temperature': request.session.get('temperature'),
        'humidity': request.session.get('humidity'),
        'ph': request.session.get('ph'),
        'rainfall': request.session.get('rainfall'),
    }

    # Ensure required data is available
    if len(crop_recommendations) < 1 or not all(soil_data.values()):
        return HttpResponse("Required data is missing.", status=400)

    # Construct the prompt with former crops and past practices
    prompt = f"""
        You are an expert agronomist specializing in sustainable and profitable farming practices in India.

        Based on the following information, create a comprehensive and detailed agricultural work plan:

        **Current Cropping Details:**
        - Previous Crops: {fcrop1}, {fcrop2}, {fcrop3}
        - Past Farming Practices: {past_practices}

        **Soil and Environmental Conditions:**
        - Nitrogen Level: {soil_data['nitrogen']} mg/kg
        - Phosphorus Level: {soil_data['phosphorus']} mg/kg
        - Potassium Level: {soil_data['potassium']} mg/kg
        - Temperature: {soil_data['temperature']}°C
        - Humidity: {soil_data['humidity']}%
        - pH Level: {soil_data['ph']}
        - Rainfall: {soil_data['rainfall']} mm/year

        **Recommended Crops for Transition:**
        - Primary Target Crop: {crop_recommendations[0]}
        - Secondary Crops: {', '.join(crop_recommendations[1:]) if len(crop_recommendations) > 1 else 'N/A'}

        **Work Plan Requirements:**
        - Develop a gradual transition plan from the existing crops to the recommended crops over appropriate timeframes.
        - Include detailed strategies for soil building and improvement, including specific techniques and amendments.
        - Outline methods for maximizing profits during and after the transition, considering market trends and crop demands.
        - Suggest simultaneous planting schemes that allow for effective and efficient transition while minimizing risks.
        - Provide seasonal schedules, resource requirements, and risk mitigation strategies.
        - Structure the plan into clear sections with headings and subheadings for easy understanding.
        - Estimate the costs associated with each part of the plan and provide a total estimated cost at the end.

        **Format:**
        Present the work plan in a structured format with sections such as:
        1. Introduction
        2. Soil Analysis and Improvement Strategies
        3. Transition Plan Overview
        4. Detailed Crop Transition Schedule
        5. Profit Maximization Strategies
        6. Simultaneous Planting Schemes
        7. Resource and Labor Management
        8. Risk Assessment and Mitigation
        9. Conclusion
        10. Estimated Costs

        Ensure that each section contains detailed and actionable information tailored to the provided conditions and requirements. Use clear and professional language suitable for implementation by farmers and agricultural planners. After the conclusion, provide a total estimated cost that will be required per year for the entire plan. Make sure to give appropriate spacing between sections, and don't ask the farmer to do research on trends or anything; you are supposed to be the solution, so you must give a suggestion. No disclaimers are allowed, and also format the text using HTML tags such as <br> and <b>.
        """


    # Generate the work plan content
    work_plan_content = generate_content(prompt, api_key)

    if not work_plan_content:
        return HttpResponse("Failed to generate work plan content.", status=500)

    # Prepare the context for rendering the template
    context = {
        'work_plan_content': work_plan_content,
        'current_date': datetime.now().strftime("%B %d, %Y"),
        'current_year': datetime.now().year,
    }

    # Render the template with the generated content
    return render(request, 'work_plan_template.html', context)


def soil_analysis(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['soil_report']
        temp_dir = 'temp'
        pdf_path = os.path.join(temp_dir, uploaded_file.name)
        
        with open(pdf_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        try:
            soil_report_text = extract_text_from_pdf(pdf_path)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
        api_key = os.getenv("GOOGLE_API_KEY")
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(
                f"Assume you are an expert in soil science and you have been asked to analyze the following soil report: {soil_report_text}. "
                f"Provide a detailed analysis and recommendations for improving soil health based on the provided report. "
                f"Return the text in a human understandable language, suitable for a farmer, without any special characters such as # /n or ** in the response."
            )
            
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
            
            # Format the generated text
            formatted_text = format_generated_text(generated_text)
            
            context = {
                'generated_text': formatted_text,
                'soil_report_text': soil_report_text
            }
            
            # Render the PDF and automatically download it
            pdf = render_to_pdf('pdf_template.html', context, 'Soil_Analysis_Report.pdf')
            if pdf:
                return pdf
            return HttpResponse("Failed to generate PDF.", status=500)
        
        except Exception as e:
            return render(request, 'pdf.html', {'error': str(e)})
        
        finally:
            if os.path.exists(pdf_path):
                os.remove(pdf_path)
    
    return render(request, 'pdf1.html')

