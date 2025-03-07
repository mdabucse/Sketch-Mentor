from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from pydantic import BaseModel
import logging
from VisualAgent.config import Config
from VisualAgent.pipeline import AgenticPipeline

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, you can restrict this to specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Setup logging and initialize clients on startup
logger = Config.setup_logging()
logger.info("Starting the agentic visualization system.")

gemini_flash_model, gemini_learn_model, openrouter_client = Config.initialize_clients()
qwen_model = Config.QWEN_MODEL
logger.info("API clients initialized successfully.")

# Create pipeline
pipeline = AgenticPipeline(gemini_flash_model, gemini_learn_model, openrouter_client, qwen_model)
logger.info("Agentic pipeline created.")

# Request model
class VisualizationRequest(BaseModel):
    prompt: str

# Response model
class VisualizationResponse(BaseModel):
    generated_code: str

@app.post("/generateVisual", response_model=VisualizationResponse)
def generate_visualization(request: VisualizationRequest):
    logger.info(f"Processing user prompt: {request.prompt}")
    try:
        generated_code = pipeline.run(request.prompt)
        logger.info("Code generation completed.")

        # Optionally save the generated code to a file
        # with open("generated_visualization.js", "w") as f:
        #     f.write(generated_code)
        # logger.info("Code saved to 'generated_visualization.js'")

        return VisualizationResponse(generated_code=generated_code)
    except Exception as e:
        logger.error(f"Error in generating code: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# Optional: To run the API using "uvicorn main:app" if this file is named main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)