import google.generativeai as genai
import os
import time
import sys
import itertools
import re
from dotenv import load_dotenv
from VisualAgent.config import Config
from VisualAgent.pipeline import AgenticPipeline
from SolveProblem.agent import GeminiP5JSGenerator
from SolveProblem.agent import FullcodeGenerator

class MathProblemSolver:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()
        self.api_key1 = os.environ["GEMINI_API_KEY_1"]
        self.api_key2 = os.environ["GEMINI_API_KEY_2"]
        # Create two chat sessions using the two different API keys
        self.chats = [self.create_chat(self.api_key1), self.create_chat(self.api_key2)]
        self.current_chat_index = 0  # Pointer to the current chat session
        
        # Initialize visualization pipeline
        self.gemini_flash_model, self.gemini_learn_model, self.openrouter_client = Config.initialize_clients()
        self.qwen_model = Config.QWEN_MODEL
        self.pipeline = AgenticPipeline(
            self.gemini_flash_model, self.gemini_learn_model, 
            self.openrouter_client, self.qwen_model
        )

    def create_chat(self, api_key):
        """Creates and returns a chat session using the provided API key."""
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name="gemini-1.5-pro",
            generation_config={
                "temperature": 1,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 8192,
                "response_mime_type": "text/plain",
            }
        )
        return model.start_chat(history=[])

    def fun_wait(self, duration=10):
        """Display a fun spinner animation for the specified duration (in seconds)."""
        spinner = itertools.cycle(['|', '/', '-', '\\'])
        end_time = time.time() + duration
        while time.time() < end_time:
            sys.stdout.write(next(spinner))
            sys.stdout.flush()
            time.sleep(0.1)
            sys.stdout.write('\b')

    def safe_send_message(self, prompt, max_retries=5, base_wait=10):
        """
        Send a message to the API using one of the two chat sessions.
        Alternates between API keys to avoid quota errors, with retries on ResourceExhausted errors.
        """
        attempt = 0
        while attempt < max_retries:
            current_chat = self.chats[self.current_chat_index]
            try:
                print(f"Using API key {self.current_chat_index + 1}... Processing your request... please wait ", end="", flush=True)
                self.fun_wait(base_wait)  # Wait before sending the request
                response = current_chat.send_message(prompt).text
                print("\nPausing briefly after API call...")
                self.fun_wait(base_wait)  # Pause after successful call
                self.current_chat_index = (self.current_chat_index + 1) % len(self.chats)  # Switch API key
                return response
            except Exception as e:
                if "ResourceExhausted" in str(e):
                    print(f"\nResourceExhausted error on API key {self.current_chat_index + 1}.")
                    self.current_chat_index = (self.current_chat_index + 1) % len(self.chats)
                    attempt += 1
                    wait_time = base_wait * (2 ** attempt)  # Exponential backoff
                    print(f"\nAttempt {attempt}/{max_retries}: Waiting for {wait_time} seconds before retrying...")
                    self.fun_wait(wait_time)
                else:
                    raise e
        raise Exception("Failed to process the request after multiple attempts due to resource exhaustion.")

    # Agent functions as methods
    def interpret(self, problem):
        """Rephrase the math problem and identify key components."""
        prompt = f"Rephrase this math problem and identify key components: {problem}"
        return self.safe_send_message(prompt)

    def strategize(self, problem, rephrased):
        """Choose the best method to solve the problem and explain why."""
        prompt = f"For '{problem}' and its rephrasing '{rephrased}', choose the best method and explain why."
        return self.safe_send_message(prompt)

    def solve(self, problem, strategy):
        """Solve the problem step by step using the chosen strategy."""
        prompt = f"Using '{strategy}', solve '{problem}' step by step."
        return self.safe_send_message(prompt)

    def verify(self, problem, solution):
        """Verify the solution's correctness and suggest fixes if needed."""
        prompt = f"Verify '{solution}' for '{problem}'. Is it correct? If not, suggest fixes."
        return self.safe_send_message(prompt)

    def explain(self, problem, solution):
        """Explain the solution step by step, inserting visualization tags where helpful."""
        prompt = (
            f"Explain the solution to '{problem}' clearly, step by step. "
            "Provide detailed explanations for each step and describe helpful visuals in text form without images. "
            "Where a visual representation (like a plot of y = x²) would be beneficial, insert the tag ```[visualization plot y=x2]``` "
            "with triple backticks before and after the tag to mark its placement. "
            f"Solution: {solution}"
        )
        return self.safe_send_message(prompt)

    def split_string_as_dict(self, s):
        """Splits a string into a dictionary separating code blocks (marked by triple backticks) and text."""
        parts = re.split(r'(```)', s)
        result = {}
        is_code = False  
        segment_index = 0

        for part in parts:
            if part == "```":
                is_code = not is_code
            else:
                if part.strip():
                    result[segment_index] = {
                        "type": "code" if is_code else "text",
                        "content": part
                    }
                    segment_index += 1

        return result

    def solve_math_problem(self, problem):
        """
        Solve the math problem and generate an explanation with embedded visualizations.
        This example uses a predefined explanation; you can uncomment the agent calls
        to integrate real-time API responses.
        """
        # Example of how you might integrate the agent calls:
        #
        rephrased = self.interpret(problem)
        print("\nRephrased problem:", rephrased)
        strategy = self.strategize(problem, rephrased)
        print("\nChosen strategy:", strategy)
        solution = self.solve(problem, strategy)
        print("\nSolution:", solution)
        verification = self.verify(problem, solution)
        print("\nVerification:", verification)
        if "incorrect" in verification.lower():
            solution = verification.split("corrected solution:")[-1].strip()
            print("\nCorrected Solution:", solution)
        final_explanation = self.explain(problem, solution)
        
        # Replace visualization tags with generated p5.js code
        tags = re.findall(r"\[visualization\s+(.+?)\]", final_explanation)
        for tag in tags:
            print(f"Generating visualization for: {tag}, please wait...")
            generated_code = self.pipeline.run(tag)
            final_explanation = final_explanation.replace(f"[visualization {tag}]", generated_code)
        result = self.split_string_as_dict(final_explanation)
        return result

# Test the agent with a sample math problem
# if __name__ == "__main__":
#     solver = MathProblemSolver()
#     Text_to_code = GeminiP5JSGenerator()
#     Full_code = FullcodeGenerator()
#     problem = "Solve the equation x^2 + 3x + 2 = 0"
#     final_result = solver.solve_math_problem(problem)
#     separate_Code = ""
#     for i, segment in enumerate(final_result.values()):
#         if segment["type"] == "text":
#             code = Text_to_code.generate_p5js_code(segment["content"])
#             separate_Code+=f"{i} th order/segment code\n"
#             separate_Code+=code
#         else:
#             separate_Code+=f"{i} th order/segment code\n"
#             separate_Code+=segment["content"]
#     # print(separate_Code)
#     full_code = Full_code.generate_p5js_code(separate_Code)
        
#     print("\nFinal Explanation:\n", full_code)