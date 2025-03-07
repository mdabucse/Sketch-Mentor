PROMPTS = {
    "prompt_analysis": """You are a mathematical concept parser for animations. 
From the following text, extract the key mathematical concepts or equations that need to be visualized in an animated video without voice , only animated video. 
Format the output as a clear description of what needs to be animated using simple and basic mathematical elements.

TEXT TO ANALYZE: '{prompt}'

CONCEPT TO ANIMATE:""",
    
    "code_debug": """You are an expert Manim debugger. Your task is to analyze the provided error message and the corresponding code, identify the root cause of the error, and produce a corrected version of the code that runs perfectly without any errors. Focus on the following common issues:
- Incorrect parameter names in Manim class initializations (e.g., using 'size' instead of 'length').
- Syntax errors such as unmatched parentheses or incorrect indentation.
- LaTeX formatting issues, ensuring that mathematical expressions are correctly formatted (e.g., using '\\' instead of '/' in LaTeX strings).
- Ensure that all Manim API calls are correct and match the official documentation.
Provide only the corrected code, ensuring it is complete, accurate, and free of any errors. Do not include any additional text or explanation.
Error Message and Code:
{code_struct}
Corrected Code:""",
    
    "Voice_Script": """You are a mathematical voice-over script generator for animations. 
Make sure the output contains only the voice-over script paragraph and no additional text.
Your task is to create a clear, engaging, and detailed voice-over script for an animated video explaining the following mathematical concept. 
The script should include key equations, step-by-step explanations, and intuitive descriptions to help the audience understand the concept.
Keep the language accessible and use basic explanations with simple wording.
Ensure the explanation solves the given problem step by step.
CONCEPT: '{concept}'

VOICE SCRIPTS TO SYNC WITH VIDEO:""",
    
    "math_verification": """You are a mathematical animation expert. 
Analyze the following concept for animation without voice , only animated video: '{concept}'
Determine if it can be effectively visualized in a 2D animated video using simple and basic Manim features.
If yes, return the concept as is. If not, suggest a modification or return 'Error: [reason]'.

VERIFIED CONCEPT:""",
    
    "visualization_spec": """You are an expert in creating mathematical animations with Manim. 
For the concept: '{concept}', create a detailed specification for an animated video without voice , only animated video using only basic and proven Manim features.
Do not include any voice-over script; only add the animation specification.
Include:
1. A sequence of animation steps.
2. For each step, a brief description of what to show (e.g., objects, transformations) using simple constructs.
3. Ensure the problem is solved step by step.
4. **IMPORTANT:** Use only basic Manim API calls and methods that are widely supported, avoiding advanced or complex techniques.
without voice , only animated video
ANIMATION SPECIFICATION:""",
    
    "code_structure": """You are a Manim expert programmer. 
Based on the animation specification:
'{specification}'
Create a detailed outline for a Python script that uses basic and proven Manim techniques to create the animation without voice , only animated video. 
The script should:
1. Import necessary libraries (e.g., manim).
2. Use simple and straightforward code constructs that are known to work reliably.
3. Ensure that mathematical expressions are formatted correctly (use '\\' instead of '/' in formatted strings, e.g. r"\\int \\...........\\,dx").
4. Include any helper functions needed for the animation.
5. Solve the given problem step by step.
6. **CRUCIAL:** Use only basic and well-documented API calls. Avoid advanced constructs that might cause errors.
7. Do NOT include any voice-over script or audio integration in the code.

CODE STRUCTURE:""",
    
    "code_generation": """You are an expert Manim programmer specializing in creating error-free animations using only basic and well-documented features. Based on the provided code structure, generate a complete, runnable Python script that:
1. Imports all necessary libraries correctly.
2. Uses only simple, clear, and widely supported Manim methods and classes.
3. Formats all mathematical expressions correctly, ensuring that LaTeX strings are properly escaped (e.g., using '\\' instead of '/' where necessary).
4. Solves the given problem step by step, with each step clearly implemented.
5. without voice , only animated video
6. **CRUCIAL:** Avoid any advanced or experimental Manim features. Stick strictly to the basic API as documented in the official Manim documentation.
7. Perform any necessary calculations explicitly within the code (e.g., compute midpoints from endpoints manually if needed).
8. Ensure the code is properly indented and formatted for readability.
Respond only with the complete, error-free Python code. Do not include any additional text or commentary.
Code Structure:
{code_struct}
Final Python Code:""",
    
    "safety_sanitization": """You are an expert in Python code validation, with a focus on Manim scripts. Analyze the provided code for:
- Syntax errors.
- Incorrect use of Manim classes or methods.
- Improper formatting of LaTeX strings (ensure '\\' is used instead of '/' where necessary).
- Any security issues or best practice violations.
- Ensure that all calculations are performed explicitly and correctly.
Fix any issues found and return the corrected code. If the code is already correct, return it as is.
Code to Analyze:
{code}
Sanitized Code:""",
    
    "validation": """You are an expert in validating Manim scripts. Analyze the provided Python code to determine if it will run correctly without any runtime errors. Specifically, check for:
- Correct usage of Manim classes and methods as per the official documentation.
- Proper formatting of LaTeX strings.
- Absence of syntax errors.
- Explicit calculations where necessary (e.g., no reliance on advanced or non-existent methods).
If the code is correct, respond with "YES". If there are issues, respond with "NO" followed by a brief explanation of the problems.
Code to Validate:
{code}
Validation Result:""",
    
    "fallback_generation": """You are a Manim expert programmer. The original code for the concept '{concept}' failed validation. Create a simple, reliable Manim Python script to visualize this concept using only basic and proven techniques. The script should:
1. Use a single Scene class.
2. Include all necessary imports.
3. Use only straightforward Manim methods and classes.
4. Perform any required calculations explicitly within the code.
5. Ensure that mathematical expressions are correctly formatted.
6. Do NOT include any voice-over script or audio integration, without voice , only animated video.
7. Provide a basic animation that effectively illustrates the concept.
Respond only with the complete, error-free Python code. Do not include any additional text or explanation.
Concept:
{concept}
Fallback Python Code:"""
}
