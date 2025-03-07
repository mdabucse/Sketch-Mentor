import os
import logging
from openai import OpenAI
import google.generativeai as genai

class Config:
    """Configuration class for API keys and clients."""
    
    # API Keys (ideally should be environment variables)
    GEMINI_API_KEY = "AIzaSyDog72B85_YyXRLtoAnAX6ppPt19FDKIc0"
    OPENROUTER_API_KEY = "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"
    
    # Model names
    QWEN_MODEL = "qwen/qwen2.5-vl-72b-instruct:free"
    
    @classmethod
    def setup_logging(cls):
        """Configure logging for the application."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("agentic_flow.log"),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    @classmethod
    def initialize_clients(cls):
        """Initialize and return API clients."""
        # Set up Gemini clients
        genai.configure(api_key=cls.GEMINI_API_KEY)
        gemini_flash_model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-01-21")
        gemini_learn_model = genai.GenerativeModel("learnlm-1.5-pro-experimental")
        
        # Set up OpenRouter client for Qwen
        openrouter_client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=cls.OPENROUTER_API_KEY,
        )
        
        return gemini_flash_model, gemini_learn_model, openrouter_client