from fastapi import APIRouter
import base64
from io import BytesIO
from apps.calculator.utils import analyze_image
from schema import ImageData, FlowchartRequest
from PIL import Image
import google.generativeai as genai
from dotenv import load_dotenv
import os

# Load environment variables and configure Gemini
load_dotenv()
genai.configure(api_key="AIzaSyCDWXDWku92dpkUHZkWFDsvIiTY4uzWG2s")  # Replace with your actual API key

router = APIRouter()

def generate_mermaid_code(text):
    prompt = f"""
    Convert the following text into a MermaidJS flowchart:
    '{text}' 
    Provide only the MermaidJS code without explanations.
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    if response and response.text.strip():
        return response.text.strip()
    else:
        # Return a default minimal flowchart with the input text
        return f"graph TD\n    A[{text}]"

@router.post('')
async def run(data: ImageData):
    image_data = base64.b64decode(data.image.split(",")[1])
    image_bytes = BytesIO(image_data)
    image = Image.open(image_bytes)
    responses = analyze_image(image, dict_of_vars=data.dict_of_vars)
    
    data = []
    response = None

    for response in responses:
        data.append(response)

    if response is not None:
        print('response in route: ', response)

    return {"message": "Image processed", "data": data, "status": "success"}

@router.post('/flowchart')
async def generate_flowchart(request: FlowchartRequest):
    mermaid_code = generate_mermaid_code(request.text)
    return {"mermaid_code": mermaid_code}