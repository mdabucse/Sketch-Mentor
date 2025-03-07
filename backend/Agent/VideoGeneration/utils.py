def clean_code_response(code_text):
    """
    Clean up code responses from LLMs by removing markdown formatting for Python code.
    
    Args:
        code_text (str): The code text that may contain markdown formatting
        
    Returns:
        str: Cleaned code without markdown formatting
    """
    # Split the text by markdown code block markers
    split_result = code_text.split("```")
    
    # If there are at least 3 parts (e.g., "", "code", ""), assume it's a code block
    if len(split_result) >= 3:
        # Take the content between the first and last ```
        code_block = split_result[1]
        # Split into lines to check for a language identifier
        lines = code_block.split("\n")
        # If the first line is "python" or "py", skip it
        if lines[0].strip() in ["python", "py"]:
            code_block = "\n".join(lines[1:])
        return code_block.strip()
    else:
        # If no markdown formatting is detected, return the text as-is
        return code_text.strip()