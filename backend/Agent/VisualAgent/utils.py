def clean_code_response(code_text):
    """
    Clean up code responses from LLMs by removing markdown formatting.
    
    Args:
        code_text (str): The code text that may contain markdown formatting
        
    Returns:
        str: Cleaned code without markdown formatting
    """
    # Remove any markdown code block formatting if present
    if code_text.startswith("```javascript") or code_text.startswith("```js"):
        code_text = code_text.split("```")[1]
        if code_text.startswith("javascript") or code_text.startswith("js"):
            code_text = code_text[code_text.find("\n")+1:]
    if code_text.endswith("```"):
        code_text = code_text[:-3].strip()
    
    return code_text.strip()