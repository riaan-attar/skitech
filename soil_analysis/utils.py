import os
import torch
import torch
from torchvision.models import resnet50
from PIL import Image
import torch.nn as nn
import torchvision.transforms as transforms
import matplotlib.pyplot as plt
import torch.nn as nn
import pdfplumber
from torchvision.models import resnet50
from PIL import Image
import torchvision.transforms as transforms
import re
import base64
from io import BytesIO
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
import numpy as np
from io import BytesIO
from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse

from django.template.loader import render_to_string
from django.conf import settings 
# List of class labels
class_labels = [
    'Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy',
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy',
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot',
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy',
    'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy',
    'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight',
    'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew',
    'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight',
    'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite',
    'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy'
]

# Load the model
path_model = r"soil_analysis\01_plant_diseases_classification_pytorch_rn50.pth"
model = resnet50(weights=None)
model.fc = nn.Sequential(nn.Linear(in_features=model.fc.in_features, out_features=len(class_labels)))
model.load_state_dict(torch.load(path_model,map_location=torch.device('cpu')))


model.eval()

# Define the preprocessing for the test images
preprocess = transforms.Compose([
    transforms.Resize(size=232, interpolation=transforms.InterpolationMode.BILINEAR),
    transforms.CenterCrop(size=224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
])

def predict_image(image_path):
    image = Image.open(image_path)
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    image_tensor = preprocess(image)
    image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension

    with torch.no_grad():
        outputs = model(image_tensor)
        _, predicted = torch.max(outputs, 1)
        predicted_label = class_labels[predicted.item()]
    
    # Split label into plant and disease
    plant_name, disease = predicted_label.split('___')
    
    return plant_name, disease



def extract_text_from_pdf(file_path):
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise Exception(f"Error extracting text: {str(e)}")
    


def format_generated_text(text):
    # Replace markdown bold (**text**) with HTML bold (<strong>text</strong>)
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Replace markdown italics (*text*) with HTML italics (<em>text</em>)
    text = re.sub(r'\*(.*?)\*', r'<em>\1</em>', text)
    
    # Handle any other replacements as needed
    
    return text
import os
import google.generativeai as genai
from django.conf import settings
import dotenv
import json
dotenv.load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

def generate_content(prompt, api_key):
    """
    Generates content based on the provided prompt using the genai API.

    Args:
    - prompt (str): The prompt to generate content.
    - api_key (str): The API key for authentication with genai.

    Returns:
    - str: Generated content based on the prompt.
    """
    # Configure the API client
    genai.configure(api_key=api_key)
    
    # Initialize the GenerativeModel
    model = genai.GenerativeModel('gemini-1.5-flash')

    # Generate content with the provided prompt
    response = model.generate_content(prompt)

    candidates = getattr(response, 'candidates', [])
    if candidates:
            candidate = candidates[0]
            content = getattr(candidate, 'content', {})
            parts = getattr(content, 'parts', [])
            if parts:
                generated_text = format_generated_text(parts[0].text)
            else:
                generated_text = 'No text parts found in the response'
    else:
            generated_text = 'No candidates found in the response'
        
    # Convert content to string and return it
    
    return generated_text
def get_base64_image(image_file):
    """Convert image file to a base64 encoded string."""
    file_content = image_file.read()
    base64_image = base64.b64encode(file_content).decode('utf-8')
    return f"data:image/{image_file.content_type.split('/')[1]};base64,{base64_image}"

def base64_image(image_path):
    """Convert image file to a base64 encoded string."""
    try:
        with open(image_path, "rb") as image_file:
            file_content = image_file.read()
            base64_image = base64.b64encode(file_content).decode('utf-8')
            return f"data:image/{image_path.split('.')[-1]};base64,{base64_image}"
    except Exception as e:
        raise RuntimeError(f"Error reading image file: {e}")
    


def validate_input(value, min_value=0, max_value=float('inf'), field_name="Field"):
    try:
        value = float(value)
        if not (min_value <= value <= max_value):
            raise ValidationError(f"{field_name} value should be between {min_value} and {max_value}.")
        return value
    except ValueError:
        raise ValidationError(f"{field_name} must be a number.")
    
def extract_info_from_combined_response(response, info_type):
    # Implement this function to extract specific information from the combined response
    # For example, you might split the response based on certain keywords or patterns
    # and return the relevant part for each info_type
    # Here's a simplified placeholder implementation:
    if info_type == "maturation time":
        # Extract maturation time
        pass
    elif info_type == "feasibility":
        # Extract feasibility
        pass
    elif info_type == "fertilizer":
        # Extract fertilizer recommendation
        pass
    elif info_type == "best practices":
        # Extract best practices
        pass
    return ""
"""
from django.template.loader import render_to_string
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa

def render_to_pdf(template_src, context_dict, request):
    template = render_to_string(template_src, context_dict)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(template.encode("UTF-8")), dest=result)
    if not pdf.err:
        return result.getvalue()
    return None
"""
import re

def format_generated_text(generated_text):
    # Replace ** with <strong> and add new lines before and after bold text
    formatted_text = re.sub(r'\*\*(.*?)\*\*', r'<br><strong>\1</strong><br>', generated_text)
    return formatted_text
    formatted_text = re.sub(r'###', '<br>', formatted_text)
    return formatted_text

from django.template.loader import render_to_string
from django.http import HttpResponse
from io import BytesIO
from xhtml2pdf import pisa
import os
from datetime import datetime

def render_to_pdf(template_src, context_dict):
    template = render_to_string(template_src, context_dict)
    result = BytesIO()
    pdf = pisa.CreatePDF(BytesIO(template.encode("UTF-8")), dest=result)
    if not pdf.err:
        return result.getvalue()
    return None

def generate_work_plan_pdf(request, work_plan_content):
    if not work_plan_content:
        return HttpResponse("Failed to generate work plan content.", status=500)
    
    # Format the generated content
    formatted_content = format_generated_text(work_plan_content)
    
    # Prepare the context for rendering the template
    context = {
        'work_plan_content': formatted_content,
        'current_date': datetime.now().strftime("%B %d, %Y"),
        'current_year': datetime.now().year,
    }

    # Render the PDF
    pdf = render_to_pdf('work_plan_template.html', context)
    
    if pdf:
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Agricultural_Work_Plan_{datetime.now().strftime("%Y%m%d")}.pdf"'
        return response
    else:
        return HttpResponse("Error generating PDF.", status=500)

