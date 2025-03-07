import os
import time
import google.generativeai as genai
from google.generativeai import types
from .prompt import generation_prompt_template, validation_prompt_template, full_code_generation_prompt, full_code_validation_prompt

class GeminiP5JSGenerator:
    """
    A class to generate and refine p5.js code using the Gemini API.
    Alternates between two API keys for each request.
    """
    def __init__(self):
        # Load API keys from environment variables.
        self.api_keys = [
            os.environ.get("GEMINI_API_KEY_1"),
            os.environ.get("GEMINI_API_KEY_2")
        ]
        self.key_index = 0

    def get_model(self):
        """
        Configure the Gemini API with the next API key and return the model.
        """
        genai.configure(api_key=self.api_keys[self.key_index])
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")  # Adjust model name if needed
        self.key_index = (self.key_index + 1) % len(self.api_keys)
        return model

    def call_api(self, prompt):
        """
        Call the Gemini API with the provided prompt using the non-streaming method.
        Returns the generated text.
        """
        generation_config = types.GenerationConfig(
            temperature=0.7,
            top_p=0.95,
            top_k=64,
            max_output_tokens=65536
        )
        model = self.get_model()
        try:
            response = model.generate_content(prompt, generation_config=generation_config)
            return response.text
        except Exception as e:
            print(f"Error with API key {self.api_keys[(self.key_index - 1) % len(self.api_keys)]}: {e}")
            time.sleep(1)
            model = self.get_model()
            response = model.generate_content(prompt, generation_config=generation_config)
            return response.text

    def generate_p5js_code(self, input_text):
        """
        Generate and refine p5.js code based on the provided explanation text.
        First, generate initial code using a generation prompt.
        Then, validate and refine the generated code using a validation prompt.
        Returns the final refined code as a string.
        """
        # Format the generation prompt template.
        generation_prompt = generation_prompt_template.format(input_text=input_text)
        generated_code = self.call_api(generation_prompt)
        # print("Initial p5.js code:")
        # print(generated_code)

        # Format the validation prompt template.
        validation_prompt = validation_prompt_template.format(generated_code=generated_code)
        refined_code = self.call_api(validation_prompt)
        print("Refined p5.js code:")
        print(refined_code)
        return refined_code

class FullcodeGenerator:
    """
    A class to generate and refine p5.js code using the Gemini API.
    Alternates between two API keys for each request.
    """
    def __init__(self):
        # Load API keys from environment variables.
        self.api_keys = [
            os.environ.get("GEMINI_API_KEY_1"),
            os.environ.get("GEMINI_API_KEY_2")
        ]
        self.key_index = 0

    def get_model(self):
        """
        Configure the Gemini API with the next API key and return the model.
        """
        genai.configure(api_key=self.api_keys[self.key_index])
        model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")  # Adjust model name if needed
        self.key_index = (self.key_index + 1) % len(self.api_keys)
        return model

    def call_api(self, prompt):
        """
        Call the Gemini API with the provided prompt using the non-streaming method.
        Returns the generated text.
        """
        generation_config = types.GenerationConfig(
            temperature=0.7,
            top_p=0.95,
            top_k=64,
            max_output_tokens=65536
        )
        model = self.get_model()
        try:
            response = model.generate_content(prompt, generation_config=generation_config)
            return response.text
        except Exception as e:
            print(f"Error with API key {self.api_keys[(self.key_index - 1) % len(self.api_keys)]}: {e}")
            time.sleep(1)
            model = self.get_model()
            response = model.generate_content(prompt, generation_config=generation_config)
            return response.text

    def generate_p5js_code(self, input_text):
        """
        Generate and refine p5.js code based on the provided explanation text.
        First, generate initial code using a generation prompt.
        Then, validate and refine the generated code using a validation prompt.
        Returns the final refined code as a string.
        """
        # Format the generation prompt template.
        generation_prompt = full_code_generation_prompt.format(input_text=input_text)
        generated_code = self.call_api(generation_prompt)
        # print("Initial p5.js code:")
        # print(generated_code)

        # Format the validation prompt template.
        validation_prompt = full_code_validation_prompt.format(generated_code=generated_code)
        refined_code = self.call_api(validation_prompt)
        # print("Refined p5.js code:")
        # print(refined_code)
        return refined_code

# For testing or running as a standalone script:
# if __name__ == "__main__":
#     input_text = """Let's break down the solution to the equation x² + 3x + 2 = 0 step by step:

# 1. **Identify the factors of 2 that add up to 3.**  We are looking for two numbers that, when multiplied together, equal the constant term (2) and, when added together, equal the coefficient of the x term (3).  In this case, the numbers 1 and 2 satisfy both conditions: 1 * 2 = 2 and 1 + 2 = 3.  This step is crucial for factoring the quadratic expression.

# 2. **Rewrite the equation in factored form.**  We use the numbers found in the previous step (1 and 2) to rewrite the quadratic equation in its factored form: (x + 1)(x + 2) = 0. This represents the same equation but expressed as a product of two binomials (expressions with two terms). This factorization is possible because of the distributive property of multiplication. Imagine the process of expanding (x + 1)(x + 2) back out: you'd get x² + 2x + x + 2, which simplifies to x² + 3x + 2, our original equation.

# 3. **Apply the Zero Product Property.** The Zero Product Property is a fundamental concept in algebra. It states that if the product of two or more factors is zero, then at least one of those factors *must* be equal to zero.  In our factored equation (x + 1)(x + 2) = 0,  the product of the two binomials is zero.  Therefore, either (x + 1) must equal zero, or (x + 2) must equal zero (or both can be zero).

# 4. **Solve for x in each case:** Now we solve two simple linear equations:
#     * **Case 1: x + 1 = 0**  To isolate x, we subtract 1 from both sides of the equation, giving us x = -1.
#     * **Case 2: x + 2 = 0** Similarly, we subtract 2 from both sides of this equation to get x = -2.

# 5. **State the solutions.** We've found two values of x that satisfy the original equation: x = -1 and x = -2. These are the solutions or roots of the quadratic equation.  This means that if you substitute either -1 or -2 back into the original equation x² + 3x + 2 = 0, the equation will hold true.
#     """
#     generator = GeminiP5JSGenerator()
#     generator.generate_p5js_code(input_text)
