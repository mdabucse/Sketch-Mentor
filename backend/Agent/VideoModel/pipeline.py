from .agents import (
    PromptAnalysisAgent,
    MathVerificationAgent,
    VisualizationSpecAgent,
    CodeStructureAgent,
    CodeGenerationAgent,
    CodeTestingAgent,
    CodeOptimizationAgent,
    ErrorDiagnosisAgent,
    ValidationConsensusAgent,
)
from .config import Config


class AgenticPipeline:
    """Enhanced agentic pipeline for generating mathematical visualizations."""
    
    def __init__(self):
        """Initialize the pipeline with necessary components."""
        # Setup logging
        self.logger = Config.setup_logging()
        self.logger.info("Initializing Agentic Pipeline")
        
        # Initialize clients
        gemini_flash_model, gemini_learn_model, openrouter_client = Config.initialize_clients()
        
        # Initialize agents
        self.prompt_analysis = PromptAnalysisAgent(gemini_flash_model, self.logger)
        self.math_verification = MathVerificationAgent(gemini_learn_model, self.logger)
        self.visualization_spec = VisualizationSpecAgent(openrouter_client, Config.QWEN_MODEL, self.logger)
        self.code_structure = CodeStructureAgent(openrouter_client, Config.QWEN_MODEL, self.logger)
        self.code_generation = CodeGenerationAgent(gemini_flash_model, self.logger)
        self.code_testing = CodeTestingAgent(gemini_learn_model, self.logger)
        self.code_optimization = CodeOptimizationAgent(gemini_flash_model, self.logger)
        self.error_diagnosis = ErrorDiagnosisAgent(gemini_learn_model, self.logger)
        self.validation_consensus = ValidationConsensusAgent(
            gemini_flash_model, gemini_learn_model, openrouter_client, Config.QWEN_MODEL, self.logger
        )
        
        self.logger.info("Agentic Pipeline initialized")
    
    def run(self, user_prompt):
        """Execute the enhanced agentic flow pipeline."""
        self.logger.info(f"Starting agentic flow with prompt: {user_prompt}")
        
        # Step 1: Extract mathematical concept
        equation = self.prompt_analysis.process(user_prompt)
        if "error" in equation.lower():
            self.logger.error(f"Failed at prompt analysis: {equation}")
            return {"status": "error", "stage": "prompt_analysis", "message": equation}
        
        # Step 2: Verify mathematical concept
        verified_concept = self.math_verification.process(equation)
        if "error" in verified_concept.lower():
            self.logger.error(f"Failed at math verification: {verified_concept}")
            return {"status": "error", "stage": "math_verification", "message": verified_concept}
        
        # Step 3: Generate visualization specification
        specification = self.visualization_spec.process(verified_concept)
        if "error" in specification.lower():
            self.logger.error(f"Failed at visualization spec: {specification}")
            return {"status": "error", "stage": "visualization_spec", "message": specification}
        
        # Step 4: Generate code structure
        code_struct = self.code_structure.process(specification)
        if "error" in code_struct.lower():
            self.logger.error(f"Failed at code structure: {code_struct}")
            return {"status": "error", "stage": "code_structure", "message": code_struct}
        
        # Step 5: Generate initial code
        code = self.code_generation.process(code_struct)
        if "error" in code.lower():
            self.logger.error(f"Failed at code generation: {code}")
            return {"status": "error", "stage": "code_generation", "message": code}
        
        # Step 6: Test code for potential issues
        test_results = self.code_testing.process(code)
        if not test_results.upper().startswith("CODE PASSES TESTING"):
            self.logger.warning(f"Code testing found issues: {test_results}")
            # Try to fix issues by rerunning code generation with the test results
            enhanced_struct = f"{code_struct}\n\nImportant issues to address:\n{test_results}"
            code = self.code_generation.process(enhanced_struct)
        
        # Step 7: Optimize code
        optimized_code = self.code_optimization.process(code)
        
        # Step 8: Validate final code
        validation_result = self.validation_consensus.process(optimized_code)
        
        if validation_result["result"] == "pass":
            self.logger.info("Agentic flow completed successfully.")
            return {
                "status": "success",
                "stage": "complete",
                "code": validation_result["code"],
                "score": validation_result["score"]
            }
        else:
            self.logger.warning(f"Validation failed with score {validation_result['score']}")
            
            # Try to diagnose and fix issues
            fixed_code = self.error_diagnosis.process(
                optimized_code, 
                f"Code failed validation with feedback:\n{validation_result['feedback']}"
            )
            
            # Revalidate the fixed code
            revalidation = self.validation_consensus.process(fixed_code)
            
            if revalidation["result"] == "pass":
                self.logger.info("Code fixed and validated successfully after diagnosis")
                return {
                    "status": "success",
                    "stage": "complete_after_fix",
                    "code": revalidation["code"],
                    "score": revalidation["score"]
                }
            else:
                # Final fallback - generate simpler code
                self.logger.warning("Fixed code still failed validation, generating fallback")
                fallback_code = self.validation_consensus.generate_fallback(verified_concept)
                
                return {
                    "status": "fallback",
                    "stage": "fallback_generation",
                    "code": fallback_code,
                    "original_code": optimized_code
                }
