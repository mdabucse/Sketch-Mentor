from pydantic import BaseModel
import google.generativeai as genai
from dotenv import load_dotenv
import os
import re  # For cleaning Mermaid syntax

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Pydantic Model
class FlowchartRequest(BaseModel):
    text: str

# Function to generate MermaidJS flowchart code
def generate_mermaid_code(text):
    try:
        prompt = f"""
        Convert the following text into a valid MermaidJS flowchart:

        '{text}'

        Provide only the MermaidJS code in string format. Do not include explanations or extra text.
        Ensure it follows MermaidJS v10+ syntax.
        """

        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        if response and response.text:
            mermaid_code = clean_mermaid_code(response.text.strip())
            return mermaid_code
        else:
            return "Error: No response from AI."

    except Exception as e:
        return f"Error: {str(e)}"

# Function to clean and validate Mermaid syntax
def clean_mermaid_code(code):
    code = re.sub(r"```mermaid|```", "", code).strip()  # Remove ```mermaid and ```
    
    if "flowchart" not in code:  
        return "Error: Invalid Mermaid syntax generated."
    
    return code

def flow_main(text):
    value = generate_mermaid_code(text)
    result = clean_mermaid_code(value)
    return result

    