from PIL import Image

# Convert canvas data to PIL Image
canvas_image = Image.frombytes('RGB', (20, 10), canvas_data)

variables = {
    "x": 5,
    "y": 10
    # Add any pre-assigned variables
}

from apps.calculator.utils import analyze_image

results = analyze_image(canvas_image, variables)