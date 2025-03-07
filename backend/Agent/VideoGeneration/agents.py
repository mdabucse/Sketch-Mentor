# agents.py

import logging
import time
from .utils import clean_code_response
from .prompts import PROMPTS

logger = logging.getLogger(__name__)

class PromptAnalysisAgent:
    """Agent responsible for extracting mathematical concepts from user prompts."""
    
    def __init__(self, gemini_model):
        self.model = gemini_model
    
    def process(self, prompt):
        logger.info(f"Starting prompt analysis for: {prompt}")
        try:
            response = self.model.generate_content(
                PROMPTS["prompt_analysis"].format(prompt=prompt)
            )
            concept = response.text.strip()
            logger.info(f"Extracted concept: {concept}")
            return concept
        except Exception as e:
            logger.error(f"Error in Gemini API: {str(e)}")
            return f"Error in Gemini API: {str(e)}"

class MathVerificationAgent:
    """Agent responsible for verifying mathematical correctness for animation."""
    
    def __init__(self, gemini_model):
        self.model = gemini_model
    
    def process(self, concept):
        logger.info(f"Verifying concept: {concept}")
        try:
            response = self.model.generate_content(
                PROMPTS["math_verification"].format(concept=concept)
            )
            result = response.text.strip()
            logger.info(f"Verification result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in Gemini API: {str(e)}")
            return f"Error in Gemini API: {str(e)}"

class VisualizationSpecAgent:
    """Agent responsible for creating animation specifications with voice-over."""
    
    def __init__(self, openrouter_client, model_name):
        self.client = openrouter_client
        self.model_name = model_name
    
    def process(self, concept):
        logger.info(f"Generating visualization spec for concept: {concept}")
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": PROMPTS["visualization_spec"].format(concept=concept)}]
            )
            spec = completion.choices[0].message.content.strip()
            logger.info(f"Visualization specification: {spec}")
            return spec
        except Exception as e:
            logger.error(f"Error in OpenRouter API: {str(e)}")
            return f"Error in OpenRouter API: {str(e)}"

class VoiceGenerationAgent:
    """Agent responsible for extracting mathematical concepts from user prompts."""
    
    def __init__(self, gemini_model):
        self.model = gemini_model
    
    def process(self, concept):
        logger.info(f"Generating voice script: {concept}")
        try:
            response = self.model.generate_content(
                PROMPTS["Voice_Script"].format(concept=concept)
            )
            concept = response.text.strip()
            logger.info(f"Extracted concept: {concept}")
            return concept
        except Exception as e:
            logger.error(f"Error in Gemini API: {str(e)}")
            return f"Error in Gemini API: {str(e)}"
        
class CodeStructureAgent:
    """Agent responsible for generating Manim code structure."""
    
    def __init__(self, openrouter_client, model_name):
        self.client = openrouter_client
        self.model_name = model_name
    
    def process(self, specification):
        logger.info(f"Generating code structure for spec: {specification}")
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": PROMPTS["code_structure"].format(specification=specification)}]
            )
            struct = completion.choices[0].message.content.strip()
            logger.info(f"Generated code structure: {struct}")
            if struct == "None":
                time(10)
                struct = completion.choices[0].message.content.strip()
            return struct
        except Exception as e:
            logger.error(f"Error in OpenRouter API: {str(e)}")
            return f"Error in OpenRouter API: {str(e)}"

class CodeGenerationAgent:
    """Agent responsible for generating Manim Python code."""
    
    def __init__(self, gemini_model):
        self.model = gemini_model
    
    def process(self, code_struct):
        logger.info(f"Generated code structure: {code_struct}")
        try:
            response = self.model.generate_content(
                PROMPTS["code_generation"].format(code_struct=code_struct)
            )
            code = response.text.strip()
            code = clean_code_response(code)
            logger.info(f"Generated code: {code}")
            return code
        except Exception as e:
            logger.error(f"Error in Gemini API: {str(e)}")
            return f"Error in Gemini API: {str(e)}"

class SafetySanitizationAgent:
    """Agent responsible for checking and sanitizing the Python code."""
    
    def __init__(self, gemini_model):
        self.model = gemini_model
    
    def process(self, code):
        logger.info(f"Sanitizing code: {code}")
        try:
            response = self.model.generate_content(
                PROMPTS["safety_sanitization"].format(code=code)
            )
            sanitized = response.text.strip()
            sanitized = clean_code_response(sanitized)
            logger.info(f"Sanitized code: {sanitized}")
            return sanitized
        except Exception as e:
            logger.error(f"Error in Gemini API: {str(e)}")
            return f"Error in Gemini API: {str(e)}"


class ValidationConsensusAgent:
    """Agent responsible for validating the code using multiple models."""
    
    def __init__(self, gemini_flash_model, gemini_learn_model, openrouter_client, qwen_model):
        self.gemini_flash_model = gemini_flash_model
        self.gemini_learn_model = gemini_learn_model
        self.openrouter_client = openrouter_client
        self.qwen_model = qwen_model
    
    def process(self, code):
        logger.info(f"Starting validation for code: {code}")
        try:
            gemini_flash_result = self.gemini_flash_model.generate_content(
                PROMPTS["validation"].format(code=code)
            ).text.strip()
            logger.info(f"Gemini flash validation result: {gemini_flash_result}")
            
            gemini_learn_result = self.gemini_learn_model.generate_content(
                PROMPTS["validation"].format(code=code)
            ).text.strip()
            logger.info(f"Gemini learn validation result: {gemini_learn_result}")
            
            qwen_result = self.openrouter_client.chat.completions.create(
                model=self.qwen_model,
                messages=[{"role": "user", "content": PROMPTS["validation"].format(code=code)}]
            ).choices[0].message.content.strip()
            logger.info(f"Qwen validation result: {qwen_result}")

            validations = [
                gemini_flash_result.strip().upper().startswith("YES"),
                gemini_learn_result.strip().upper().startswith("YES"),
                qwen_result.strip().upper().startswith("YES")
            ]
            
            if sum(validations) >= 2:
                logger.info("Code passed validation consensus.")
                return code
            
            reasons = []
            if not validations[0] and len(gemini_flash_result) > 3:
                reasons.append(f"Gemini Flash: {gemini_flash_result[3:].strip()}")
            if not validations[1] and len(gemini_learn_result) > 3:
                reasons.append(f"Gemini Learn: {gemini_learn_result[3:].strip()}")
            if not validations[2] and len(qwen_result) > 3:
                reasons.append(f"Qwen: {qwen_result[3:].strip()}")
                
            failure_message = "Code validation failed. " + " ".join(reasons)
            logger.warning(failure_message)
            return failure_message
        except Exception as e:
            logger.error(f"Error during validation: {str(e)}")
            return f"Error during validation: {str(e)}"
    
    def generate_fallback(self, concept):
        try:
            fallback_retry = self.gemini_flash_model.generate_content(
                PROMPTS["fallback_generation"].format(concept=concept)
            ).text.strip()
            fallback_retry = clean_code_response(fallback_retry)
            logger.info(f"Generated fallback code: {fallback_retry}")
            return fallback_retry
        except Exception as e:
            logger.error(f"Error generating fallback code: {str(e)}")
            return f"Error generating fallback code: {str(e)}"