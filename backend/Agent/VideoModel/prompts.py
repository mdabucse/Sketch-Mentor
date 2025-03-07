PROMPTS = {
    "prompt_analysis": """You are a mathematical concept parser for advanced animations. 
From the following text, extract the key mathematical concepts, equations, theorems, or problems that need to be visualized in an animated video without voice, only animated video. 
Format the output as a clear, detailed description of what needs to be animated using mathematical elements and techniques.
For complex concepts, break them down into fundamental components.

TEXT TO ANALYZE: '{prompt}'

CONCEPT TO ANIMATE:""",
    
    "math_verification": """You are a mathematical animation expert with deep knowledge of advanced mathematics. 
Analyze the following concept for animation without voice, only animated video: '{concept}'

Please do three things:
1. Verify if this concept can be effectively visualized using Manim in a 2D animated video
2. Formalize any equations or mathematical expressions that will be needed
3. Identify any complex calculations that might be required

If the concept is suitable for visualization, return a structured response with:
- Verified concept description
- Formalized mathematical expressions
- Required calculations

If not suitable, explain why and suggest modifications to make it animatable.

VERIFIED CONCEPT:""",
    
    "visualization_spec": """You are an expert in creating mathematical animations with Manim for advanced mathematical concepts. 
For the concept: '{concept}', create a detailed specification for an animated video without voice, only animated video using Manim.

Include:
1. A sequence of animation steps, broken down into logical scenes or sections
2. For each step, specify:
   - What mathematical objects to create (equations, graphs, geometric shapes, vectors, etc.)
   - What transformations to apply (appear, transform, move, highlight, etc.)
   - What colors, styles, and positioning to use
3. Ensure the problem/concept is visualized step by step with clear progression
4. Specify any special effects or techniques needed (e.g., zooming, coordinate systems, 3D elements if appropriate)
5. Indicate appropriate timing or pacing for complex elements

Use only Manim features and techniques that are well-documented and reliable.

ANIMATION SPECIFICATION:""",
    
    "code_structure": """You are a Manim expert programmer specializing in visualizing advanced mathematical concepts. 
Based on the animation specification:
'{specification}'

Create a detailed outline for a Python script that uses Manim to create the animation. The structure should:

1. Define all necessary imports (manim and other required libraries)
2. Organize the animation into appropriate Scene classes and helper methods
3. Include detailed comments explaining the mathematical implementation
4. Structure the code to handle any complex calculations or transformations
5. Ensure proper setup for any coordinate systems, 3D spaces, or special visualizations
6. Include error handling for potentially complex operations

Your outline should be comprehensive but focus on creating maintainable, error-free code that follows Manim best practices. Do not include any voice-over functionality.

CODE STRUCTURE:""",
    
    "code_generation": """You are an expert Manim programmer specializing in creating error-free animations for advanced mathematical concepts. Based on the provided code structure, generate a complete, runnable Python script that:

1. Implements all necessary Manim classes, methods, and calculations correctly
2. Uses appropriate Manim features for each visualization component
3. Formats all mathematical expressions correctly using proper LaTeX syntax
4. Includes robust error handling for complex operations
5. Provides clear, detailed comments explaining the mathematical implementation
6. Ensures proper timing and sequencing of animations
7. Optimizes performance for complex visualizations

IMPORTANT GUIDELINES:
- Format LaTeX expressions correctly (use '\\\\' for LaTeX escape sequences)
- Use explicit coordinates and calculations where needed
- Avoid deprecated Manim methods or classes
- Include fallback methods for complex operations that might fail
- Ensure proper indentation and code style

Code Structure:
{code_struct}

Final Python Code:""",
    
    "code_testing": """You are a Manim testing expert. Analyze the following code for potential runtime errors, logical issues, or incorrect Manim API usage. 

Focus on these common issues:
1. Incorrect parameter types or names in Manim functions
2. Missing or incorrect imports
3. LaTeX formatting errors
4. Calculation errors in mathematical operations
5. Issues with animation sequencing or timing
6. Potential performance problems with complex visualizations

Code to test:
{code}

For each issue found, provide:
1. The specific line or section with the issue
2. What the problem is
3. How to fix it

If no issues are found, respond with "CODE PASSES TESTING".

TESTING RESULTS:""",
    
    "code_optimization": """You are a Manim optimization expert. Analyze and improve the following code for better performance, readability, and reliability without changing its core functionality.

Focus on:
1. Reducing redundant calculations
2. Improving animation performance
3. Enhancing code readability and structure
4. Adding appropriate error handling
5. Ensuring mathematical accuracy

Code to optimize:
{code}

Provide the optimized code version with comments explaining key optimizations.

OPTIMIZED CODE:""",
    
    "error_diagnosis": """You are a Manim debugging expert. Analyze the following error that occurred when running Manim code:

Error message:
{error}

Code that produced the error:
{code}

Please provide:
1. A detailed explanation of what caused the error
2. The exact location in the code where the error occurred
3. A specific fix for the issue
4. Any additional recommendations to prevent similar errors

DIAGNOSIS AND FIX:""",
    
    "fallback_generation": """You are a Manim expert programmer. The original code for the concept '{concept}' encountered issues. Create a simplified, ultra-reliable Manim Python script that:

1. Uses only the most basic and proven Manim techniques
2. Focuses on visualizing just the core aspects of the concept
3. Includes extensive error handling
4. Uses explicit calculations rather than relying on advanced API features
5. Formats all mathematical expressions conservatively

Prioritize creating code that will run without errors over implementing all details of the original concept.

RELIABLE FALLBACK CODE:""",
    
    "validation_consensus": """You are evaluating a Manim code implementation for correctness and reliability. Review the code carefully and answer the following questions:

1. Does the code correctly implement the mathematical concept?
2. Are all Manim methods and functions used correctly?
3. Is the animation sequence logical and clear?
4. Are there any potential runtime errors or exceptions?
5. Is the code well-structured and maintainable?

Code to validate:
{code}

Respond with YES or NO to each question, followed by a brief explanation.

VALIDATION RESULTS:"""
}