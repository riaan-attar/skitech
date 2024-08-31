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
model.load_state_dict(torch.load(path_model))


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