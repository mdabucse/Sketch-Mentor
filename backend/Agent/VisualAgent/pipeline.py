import logging
from .agents import (
    PromptAnalysisAgent,
    MathVerificationAgent,
    VisualizationSpecAgent,
    CodeStructureAgent,
    CodeGenerationAgent,
    SafetySanitizationAgent,
    ValidationConsensusAgent
)

logger = logging.getLogger(__name__)
class AgenticPipeline:
    """Coordinates the agentic flow for generating p5.js visualization code."""
    
    def __init__(self, gemini_flash_model, gemini_learn_model, openrouter_client, qwen_model):
        """Initialize the pipeline with the required models and clients."""
        self.prompt_analysis = PromptAnalysisAgent(gemini_flash_model)
        self.math_verification = MathVerificationAgent(gemini_learn_model)
        self.visualization_spec = VisualizationSpecAgent(openrouter_client, qwen_model)
        self.code_structure = CodeStructureAgent(openrouter_client, qwen_model)
        self.code_generation = CodeGenerationAgent(openrouter_client, qwen_model)
        self.safety_sanitization = SafetySanitizationAgent(gemini_flash_model)
        self.validation_consensus = ValidationConsensusAgent(
            gemini_flash_model, gemini_learn_model, openrouter_client, qwen_model
        )
    
    def run(self, user_prompt):
        """Execute the full agentic flow pipeline."""
        logger.info(f"Starting agentic flow with prompt: {user_prompt}")
        
        # Step 1: Extract equation
        equation = self.prompt_analysis.process(user_prompt)
        if "error" in equation.lower():
            logger.error(f"Failed at prompt analysis: {equation}")
            return equation
        logger.info(f"Step 1 completed: {equation}")

        # Step 2: Verify equation
        verified_equation = self.math_verification.process(equation)
        if verified_equation.lower().startswith("error:"):
            logger.error(f"Failed at math verification: {verified_equation}")
            return verified_equation
        logger.info(f"Step 2 completed: {verified_equation}")

        # Step 3: Specify visualization
        specification = self.visualization_spec.process(verified_equation)
        if "error" in specification.lower():
            logger.error(f"Failed at visualization spec: {specification}")
            return specification
        logger.info(f"Step 3 completed: {specification}")

        # Step 4: Generate code structure
        code_struct = self.code_structure.process(specification)
        if "error" in code_struct.lower():
            logger.error(f"Failed at code structure: {code_struct}")
            return code_struct
        logger.info(f"Step 4 completed: {code_struct}")

        # Step 5: Generate code
        code = self.code_generation.process(code_struct)
        if "error" in code.lower():
            logger.error(f"Failed at code generation: {code}")
            return code
        logger.info(f"Step 5 completed: {code}")

        # Step 6: Sanitize code
        sanitized_code = self.safety_sanitization.process(code)
        if "vulnerabilities" in sanitized_code.lower() or "error" in sanitized_code.lower():
            logger.error(f"Failed at sanitization: {sanitized_code}")
            return sanitized_code
        logger.info(f"Step 6 completed: {sanitized_code}")

        # Step 7: Validate code
        validated_code = self.validation_consensus.process(sanitized_code)
        if "failed" in validated_code.lower():
            logger.error(f"Failed at validation: {validated_code}")
            
            # Try one more time with a fallback approach for common equations
            return self.validation_consensus.generate_fallback(verified_equation)
        
        logger.info("Agentic flow completed successfully.")
        return validated_code