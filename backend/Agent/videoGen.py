from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import logging
import os
import subprocess
from pathlib import Path
import textwrap
from VideoGeneration.utils import clean_code_response
from VideoGeneration.config import Config
from VideoGeneration.pipeline import AgenticPipeline
from VideoGeneration.prompts import PROMPTS
from fastapi.staticfiles import StaticFiles

# Initialize FastAPI app
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your needs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup logging via your configuration
logger = Config.setup_logging()

# Define a Pydantic model for the request payload.
class VisualizationRequest(BaseModel):
    problem: str

def save_code_safely(code_content: str, filename: str) -> bool:
    """
    Save generated code with ASCII-safe characters only.
    """
    try:
        # Normalize line endings.
        clean_content = '\n'.join(code_content.splitlines())
        # Encode to ASCII (replacing non-ASCII characters) then decode back.
        clean_content = clean_content.encode('ascii', 'replace').decode('ascii')
        Path(filename).write_text(clean_content)
        return True
    except Exception as e:
        logger.error(f"Error saving file: {str(e)}")
        return False

# --- The CodeGenerationAgent as provided ---
class CodeGenerationAgent:
    """Agent responsible for generating Manim Python code."""
    
    def __init__(self, openrouter_client, model_name):
        self.client = openrouter_client
        self.model_name = model_name
    
    def process(self, code_struct):
        logger.info(f"Generating Manim code from structure: {code_struct}")
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": PROMPTS["code_debug"].format(code_struct=code_struct)}]
            )
            code = completion.choices[0].message.content.strip()
            code = clean_code_response(code)  # Assumes a helper to clean up the response
            logger.info(f"Generated Manim code: {code}")
            return code
        except Exception as e:
            logger.error(f"Error in OpenRouter API: {str(e)}")
            return f"Error in OpenRouter API: {str(e)}"

@app.post("/videoGeneration")
def visualize(req: VisualizationRequest):
    """
    Generate a visualization video for a given mathematical problem.
    This endpoint will generate Manim code, run it, and if an error occurs during rendering,
    it will use the CodeGenerationAgent to debug the code—identifying issues such as the MiKTeX update
    warning causing LaTeX conversion errors—and provide corrected code until successful.
    """
    logger.info(f"Received visualization request for problem: {req.problem}")
    
    try:
        # Initialize API clients
        gemini_flash_model, gemini_learn_model, openrouter_client = Config.initialize_clients()
        qwen_model = Config.QWEN_MODEL
        logger.info("API clients initialized successfully.")
        print("API clients initialized successfully.")
        # Create the initial pipeline.
        pipeline = AgenticPipeline(gemini_flash_model, gemini_learn_model, openrouter_client, qwen_model)
        logger.info("Agentic pipeline created.")
        print("Agentic pipeline created.")
        # Generate the initial Manim code.
        generated_code = pipeline.run(req.problem)
        logger.info("Initial code generation completed.")
        generated_code = textwrap.dedent(generated_code)
        print("============================"+generated_code)
        file_name = "Visualization_Video.py"
        max_retries = 3
        attempt = 0
        
        # Initialize the code correction agent.
        code_agent = CodeGenerationAgent(openrouter_client, qwen_model)
        if not save_code_safely(generated_code, file_name):
            logger.error("Failed to save generated code.")
            raise HTTPException(status_code=500, detail="Failed to save generated code.")
        # Loop until the Manim command runs successfully or the max number of retries is reached.
        while attempt < max_retries:
            attempt += 1
            logger.info(f"Attempt {attempt}: Saving code to file.")
            
            # Define the scene name (the generated code must define a Scene class with this name).
            scene_name = "VisualizationVideo"
            manim_command = ["manim", "-pql", file_name, scene_name]
            logger.info(f"Running Manim command: {' '.join(manim_command)}")
            
            result = subprocess.run(manim_command, capture_output=True, text=True)
            if result.returncode == 0:
                logger.info("Manim rendering completed successfully.")
                break  # Exit loop if rendering is successful.
            else:
                logger.error(f"Manim failed on attempt {attempt}: {result.stderr}")
                # Build a prompt that includes the error details and the problematic code,
                # instructing the agent to debug the issue—including the MiKTeX update warning causing LaTeX conversion errors.
                code_struct = (
                    f"goal is to animate the following mathematical concept: {req.problem}\n "
                    f"Error: {result.stderr}\n"
                    f"Code that caused the error:\n{generated_code}\n"
                    "Please debug this code by identifying the root cause of the error, including addressing the MiKTeX update warning "
                    "that causes LaTeX conversion to dvi to fail, and provide updated code that runs perfectly without this error."
                    "if the error is cant solvable give me a simple animation to solve the problem {req.problem}"
                )
                # Use the AI agent to generate a corrected (debugged) version of the code.
                corrected_code = code_agent.process(code_struct)
                generated_code = textwrap.dedent(corrected_code)
                logger.info("Generated corrected (debugged) code using CodeGenerationAgent.")
        
        if attempt == max_retries and result.returncode != 0:
            logger.error("Exceeded maximum attempts to correct code.")
            raise HTTPException(status_code=500, detail=f"Manim error after {max_retries} attempts: {result.stderr}")
        
        # Build the expected video file path.
        base_name = os.path.splitext(file_name)[0]
        quality = "480p15"  # Adjust if you use a different quality flag.
        video_path = f"http://localhost:8000/media/videos/{base_name}/{quality}/{scene_name}.mp4"
        logger.info(f"Video generated at: {video_path}")
        
        return {"video_path": video_path}
    
    except Exception as e:
        logger.error(f"Error in visualization: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))