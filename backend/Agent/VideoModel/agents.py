from .utils import Utils
import time
from VideoModel.prompts import PROMPTS


class BaseAgent:
    """Base class for all agents in the pipeline."""
    
    def __init__(self, name, logger):
        self.name = name
        self.logger = logger
    
    def log_start(self, message):
        self.logger.info(f"[{self.name}] Starting: {message}")
    
    def log_complete(self, message):
        self.logger.info(f"[{self.name}] Completed: {message}")
    
    def log_error(self, message):
        self.logger.error(f"[{self.name}] Error: {message}")


class PromptAnalysisAgent(BaseAgent):
    """Agent responsible for extracting mathematical concepts from user prompts."""
    
    def __init__(self, gemini_model, logger):
        super().__init__("PromptAnalysis", logger)
        self.model = gemini_model
    
    def process(self, prompt):
        self.log_start(f"Analyzing prompt: {prompt}")
        try:
            response = self.model.generate_content(
                PROMPTS["prompt_analysis"].format(prompt=prompt)
            )
            concept = response.text.strip()
            self.log_complete(f"Extracted concept: {concept}")
            return concept
        except Exception as e:
            self.log_error(f"API error: {str(e)}")
            return f"Error in concept extraction: {str(e)}"


class MathVerificationAgent(BaseAgent):
    """Agent responsible for verifying mathematical correctness for animation."""
    
    def __init__(self, gemini_model, logger):
        super().__init__("MathVerification", logger)
        self.model = gemini_model
    
    def process(self, concept):
        self.log_start(f"Verifying concept: {concept}")
        try:
            response = self.model.generate_content(
                PROMPTS["math_verification"].format(concept=concept)
            )
            result = response.text.strip()
            self.log_complete(f"Verification result: {result}")
            return result
        except Exception as e:
            self.log_error(f"API error: {str(e)}")
            return f"Error in math verification: {str(e)}"


class VisualizationSpecAgent(BaseAgent):
    """Agent responsible for creating animation specifications."""
    
    def __init__(self, openrouter_client, model_name, logger):
        super().__init__("VisualizationSpec", logger)
        self.client = openrouter_client
        self.model_name = model_name
    
    def process(self, concept):
        self.log_start(f"Generating visualization spec for: {concept}")
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": PROMPTS["visualization_spec"].format(concept=concept)}]
            )
            spec = completion.choices[0].message.content.strip()
            self.log_complete(f"Generated visualization specification")
            return spec
        except Exception as e:
            self.log_error(f"API error: {str(e)}")
            return f"Error in visualization specification: {str(e)}"


class CodeStructureAgent(BaseAgent):
    """Agent responsible for generating Manim code structure."""
    
    def __init__(self, openrouter_client, model_name, logger):
        super().__init__("CodeStructure", logger)
        self.client = openrouter_client
        self.model_name = model_name
    
    def process(self, specification):
        self.log_start(f"Generating code structure")
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": PROMPTS["code_structure"].format(specification=specification)}]
            )
            struct = completion.choices[0].message.content.strip()
            self.log_complete(f"Generated code structure")
            
            # Retry if the response is empty or "None"
            if struct.lower() == "none" or not struct:
                self.logger.warning("Empty structure received, retrying...")
                time.sleep(5)
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": PROMPTS["code_structure"].format(specification=specification)}]
                )
                struct = completion.choices[0].message.content.strip()
                self.log_complete(f"Generated code structure on retry")
            
            return struct
        except Exception as e:
            self.log_error(f"API error: {str(e)}")
            return f"Error in code structure generation: {str(e)}"


class CodeGenerationAgent(BaseAgent):
    """Agent responsible for generating Manim Python code."""
    
    def __init__(self, gemini_model, logger):
        super().__init__("CodeGeneration", logger)
        self.model = gemini_model
    
    def process(self, code_struct):
        self.log_start(f"Generating code")
        try:
            response = self.model.generate_content(
                PROMPTS["code_generation"].format(code_struct=code_struct)
            )
            code = response.text.strip()
            code = Utils.clean_code_response(code)
            self.log_complete(f"Generated code")
            return code
        except Exception as e:
            self.log_error(f"API error: {str(e)}")
            return f"Error in code generation: {str(e)}"


class CodeTestingAgent(BaseAgent):
    """Agent responsible for testing code for potential issues."""
    
    def __init__(self, gemini_model, logger):
        super().__init__("CodeTesting", logger)
        self.model = gemini_model
    
    def process(self, code):
        self.log_start(f"Testing code")
        try:
            response = self.model.generate_content(
                PROMPTS["code_testing"].format(code=code)
            )
            result = response.text.strip()
            self.log_complete(f"Testing results: {result[:100]}...")
            return result
        except Exception as e:
            self.log_error(f"API error: {str(e)}")
            return f"Error in code testing: {str(e)}"


class CodeOptimizationAgent(BaseAgent):
    """Agent responsible for optimizing the generated code."""
    
    def __init__(self, gemini_model, logger):
        super().__init__("CodeOptimization", logger)
        self.model = gemini_model
    
    def process(self, code):
        self.log_start(f"Optimizing code")
        try:
            response = self.model.generate_content(
                PROMPTS["code_optimization"].format(code=code)
            )
            optimized = Utils.clean_code_response(response.text.strip())
            self.log_complete(f"Optimized code")
            return optimized
        except Exception as e:
            self.log_error(f"API error: {str(e)}")
            return code  # Return original code if optimization fails


class ErrorDiagnosisAgent(BaseAgent):
    """Agent responsible for diagnosing and fixing errors in code."""
    
    def __init__(self, gemini_model, logger):
        super().__init__("ErrorDiagnosis", logger)
        self.model = gemini_model
    
    def process(self, code, error):
        self.log_start(f"Diagnosing error: {error[:100]}...")
        try:
            response = self.model.generate_content(
                PROMPTS["error_diagnosis"].format(code=code, error=error)
            )
            diagnosis = response.text.strip()
            
            # Try to extract fixed code
            fixed_code = Utils.clean_code_response(diagnosis)
            if fixed_code and len(fixed_code) > 100:  # Basic check if we got actual code
                self.log_complete(f"Error fixed")
                return fixed_code
            else:
                self.log_error(f"Failed to extract fixed code")
                return code  # Return original code if no fix was found
                
        except Exception as e:
            self.log_error(f"API error: {str(e)}")
            return code  # Return original code if diagnosis fails


class ValidationConsensusAgent(BaseAgent):
    """Agent responsible for validating the code using multiple models."""
    
    def __init__(self, gemini_flash_model, gemini_learn_model, openrouter_client, qwen_model, logger):
        super().__init__("ValidationConsensus", logger)
        self.gemini_flash_model = gemini_flash_model
        self.gemini_learn_model = gemini_learn_model
        self.openrouter_client = openrouter_client
        self.qwen_model = qwen_model
    
    def process(self, code):
        self.log_start(f"Validating code")
        
        validation_results = []
        validators = [
            ("Gemini Flash", self.gemini_flash_model, True),
            ("Gemini Learn", self.gemini_learn_model, True),
            ("Qwen", None, False)
        ]
        
        for name, model, is_gemini in validators:
            try:
                if is_gemini:
                    response = model.generate_content(
                        PROMPTS["validation_consensus"].format(code=code)
                    ).text.strip()
                else:
                    response = self.openrouter_client.chat.completions.create(
                        model=self.qwen_model,
                        messages=[{"role": "user", "content": PROMPTS["validation_consensus"].format(code=code)}]
                    ).choices[0].message.content.strip()
                
                # Parse validation response
                lines = response.split('\n')
                yes_count = 0
                for line in lines:
                    if line.strip().upper().startswith("YES"):
                        yes_count += 1
                
                validation_results.append({
                    "validator": name,
                    "pass_rate": yes_count / 5,  # 5 questions in the prompt
                    "response": response
                })
                
                self.logger.info(f"[{name}] Validation score: {yes_count/5}")
                
            except Exception as e:
                self.log_error(f"Error with {name} validator: {str(e)}")
                validation_results.append({
                    "validator": name,
                    "pass_rate": 0,
                    "response": f"Error: {str(e)}"
                })
        
        # Calculate average validation score
        avg_score = sum(v["pass_rate"] for v in validation_results) / len(validation_results)
        self.log_complete(f"Validation complete. Average score: {avg_score}")
        
        if avg_score >= 0.6:  # At least 60% pass rate
            return {"result": "pass", "code": code, "score": avg_score}
        else:
            return {
                "result": "fail", 
                "code": code, 
                "score": avg_score,
                "feedback": "\n".join([f"{v['validator']}: {v['response']}" for v in validation_results])
            }
    
    def generate_fallback(self, concept):
        self.log_start(f"Generating fallback code for: {concept}")
        try:
            response = self.gemini_flash_model.generate_content(
                PROMPTS["fallback_generation"].format(concept=concept)
            ).text.strip()
            fallback_code = Utils.clean_code_response(response)
            self.log_complete(f"Generated fallback code")
            return fallback_code
        except Exception as e:
            self.log_error(f"Error generating fallback: {str(e)}")
            return f"Error generating fallback code: {str(e)}"