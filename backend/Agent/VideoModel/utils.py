import re


class Utils:
    @staticmethod
    def clean_code_response(response):
        """Clean and extract code blocks from LLM responses."""
        # Extract code from markdown code blocks if present
        code_block_pattern = r"```python\s*([\s\S]*?)\s*```"
        code_blocks = re.findall(code_block_pattern, response)
        
        if code_blocks:
            return code_blocks[0].strip()
        
        # If no code blocks found, return the original response
        return response
    
    @staticmethod
    def extract_error_message(error_text):
        """Extract the core error message from a Python traceback."""
        error_pattern = r"(?:Error|Exception):\s*(.*?)(?:\n|$)"
        match = re.search(error_pattern, error_text)
        if match:
            return match.group(1)
        return error_text
    
    @staticmethod
    def extract_function_definitions(code):
        """Extract function and class definitions from code."""
        function_pattern = r"(def\s+\w+\([^)]*\)\s*:[\s\S]*?)(?=\s*def|\s*class|\Z)"
        class_pattern = r"(class\s+\w+(?:\([^)]*\))?\s*:[\s\S]*?)(?=\s*def|\s*class|\Z)"
        
        functions = re.findall(function_pattern, code)
        classes = re.findall(class_pattern, code)
        
        return functions + classes