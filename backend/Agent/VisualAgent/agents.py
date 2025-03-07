import logging
from .utils import clean_code_response
from .prompts import PROMPTS

logger = logging.getLogger(__name__)

class PromptAnalysisAgent:
    """Agent responsible for extracting mathematical equations from user prompts."""
    
    def __init__(self, gemini_model):
        self.model = gemini_model
    
    def process(self, prompt):
        """Extract the mathematical equation from the user prompt."""
        logger.info(f"Starting prompt analysis for: {prompt}")
        try:
            response = self.model.generate_content(
                PROMPTS["prompt_analysis"].format(prompt=prompt)
            )
            equation = response.text.strip()
            logger.info(f"Extracted equation From Gemini: {equation}")
            return equation
        except Exception as e:
            logger.error(f"Error in Gemini API: {str(e)}")
            return f"Error in Gemini API: {str(e)}"


class MathVerificationAgent:
    """Agent responsible for verifying mathematical correctness of equations."""
    
    def __init__(self, gemini_model):
        self.model = gemini_model
    
    def process(self, equation):
        """Verify the mathematical correctness of the equation."""
        logger.info(f"Verifying equation: {equation}")
        try:
            response = self.model.generate_content(
                PROMPTS["math_verification"].format(equation=equation)
            )
            result = response.text.strip()
            logger.info(f"Verification result: {result}")
            return result
        except Exception as e:
            logger.error(f"Error in Gemini API: {str(e)}")
            return f"Error in Gemini API: {str(e)}"


class VisualizationSpecAgent:
    """Agent responsible for creating visualization specifications."""
    
    def __init__(self, openrouter_client, model_name):
        self.client = openrouter_client
        self.model_name = model_name
    
    def process(self, equation):
        """Create a visualization specification for the equation."""
        logger.info(f"Generating visualization spec for equation: {equation}")
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "user",
                    "content": PROMPTS["visualization_spec"].format(equation=equation)
                }]
            )
            spec = completion.choices[0].message.content.strip()
            logger.info(f"Visualization specification: {spec}")
            return spec
        except Exception as e:
            logger.error(f"Error in OpenRouter API: {str(e)}")
            return f"Error in OpenRouter API: {str(e)}"


class CodeStructureAgent:
    """Agent responsible for generating code structure."""
    
    def __init__(self, openrouter_client, model_name):
        self.client = openrouter_client
        self.model_name = model_name
    
    def process(self, specification):
        """Generate code structure based on visualization specification."""
        logger.info(f"Generating code structure for spec: {specification}")
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "user",
                    "content": PROMPTS["code_structure"].format(specification=specification)
                }]
            )
            struct = completion.choices[0].message.content.strip()
            logger.info(f"Generated code structure: {struct}")
            return struct
        except Exception as e:
            logger.error(f"Error in OpenRouter API: {str(e)}")
            return f"Error in OpenRouter API: {str(e)}"


class CodeGenerationAgent:
    """Agent responsible for generating p5.js code."""
    
    def __init__(self, openrouter_client, model_name):
        self.client = openrouter_client
        self.model_name = model_name
    
    def process(self, code_struct):
        """Generate p5.js code based on code structure."""
        logger.info(f"Generating p5.js code from structure: {code_struct}")
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{
                    "role": "user",
                    "content": PROMPTS["code_generation"].format(code_struct=code_struct)
                }]
            )
            code = completion.choices[0].message.content.strip()
            # Remove any markdown code block formatting if present
            code = clean_code_response(code)
            logger.info(f"Generated p5.js code: {code}")
            return code
        except Exception as e:
            logger.error(f"Error in OpenRouter API: {str(e)}")
            return f"Error in OpenRouter API: {str(e)}"


class SafetySanitizationAgent:
    """Agent responsible for checking and sanitizing the code."""
    
    def __init__(self, gemini_model):
        self.model = gemini_model
    
    def process(self, code):
        """Check and sanitize the p5.js code."""
        logger.info(f"Sanitizing code: {code}")
        try:
            response = self.model.generate_content(
                PROMPTS["safety_sanitization"].format(code=code)
            )
            sanitized = response.text.strip()
            # Remove any markdown code block formatting if present
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
        """Validate the code using all three models."""
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
                messages=[{"role": "user", "content": 
                    PROMPTS["validation"].format(code=code)
                }]
            ).choices[0].message.content.strip()
            logger.info(f"Qwen validation result: {qwen_result}")

            # Check if at least 2 out of 3 models say YES
            validations = [
                gemini_flash_result.strip().upper().startswith("YES"),
                gemini_learn_result.strip().upper().startswith("YES"),
                qwen_result.strip().upper().startswith("YES")
            ]
            
            if sum(validations) >= 2:
                logger.info("Code passed validation consensus.")
                return code
            
            # If code failed validation, collect reasons
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
    
    def generate_fallback(self, equation):
        """Generate fallback code for common equations when validation fails."""
        try:
            fallback_retry = self.gemini_flash_model.generate_content(
                PROMPTS["fallback_generation"].format(equation=equation)
            ).text.strip()
            
            # Remove any markdown code block formatting if present
            fallback_retry = clean_code_response(fallback_retry)
            logger.info(f"Generated fallback code: {fallback_retry}")
            return fallback_retry
        except Exception as e:
            logger.error(f"Error generating fallback code: {str(e)}")
            return f"Error generating fallback code: {str(e)}"