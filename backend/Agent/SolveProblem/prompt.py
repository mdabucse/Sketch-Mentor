# prompt.py

generation_prompt_template = """
Given the following explanation text, generate a p5.js sketch that displays it using DOM elements (no canvas) with HTML and CSS formatting.
Convert any markdown-like formatting in the text to appropriate HTML tags, such as <strong> for bold, <em> for italics, and <code> for inline code or math expressions.
Structure the text using HTML elements like <h2>, <ol>, <li>, etc., as needed.
Include comments in the code for clarity.
Provide the complete `function setup()` code as a plain text response.

Explanation text:
{input_text}
"""

validation_prompt_template = """
Review the following p5.js code intended to display a text explanation using DOM elements.
Check for any syntax errors, ensure that the HTML and CSS are correctly applied, and verify that the text is properly formatted with appropriate HTML tags.
Suggest improvements to make the code clean, efficient, and robust.
Provide the refined `function setup()` code as a plain text response.
strictly give a P5.js code only as output nothing else.
don't explain anything.
dont add any comments and dont add style tag use only p5.js.
dont give a incomplete code.
only give a P5.js code only as output nothing else no other words(```p5.js ,```javascript) at all.
Generated code:
{generated_code}
"""
# prompt.py
full_code_generation_prompt = """ You are an expert coder in p5.js. Combine the separate p5.js code snippets provided in {input_text} into a single, fully functional p5.js sketch. Your task is to integrate the separate segments exactly in the order they are provided, ensuring that the display order (e.g., text, visual, text) remains unchanged. Do not reorder any segments (for example, do not place visual elements before text if they are provided later). Combine these codes as a single p5.js code and output only the p5.js code without any additional text, explanations, comments, or markdown markers. Ensure that visual elements (canvas or DOM) are arranged to prevent any overlapping, resulting in a clean and perfect layout. Use advanced techniques such as creating a main container with a natural document flow (e.g., CSS Flexbox or Grid) via p5.js’s createDiv() method. Append each segment (text, canvas, additional text) as children of this container so that the browser’s inherent layout flow preserves the original order provided in the input. Maintain the exact order of the given code snippets, integrating them sequentially without modifying their sequence. Do not alter the order of visual elements; they must appear exactly as provided. Position and style any visual elements (canvas or DOM) to prevent unintended overlapping. Important: Maintain the display based on the segments. Segment order needs to follow strictly and display the code segments in the same order as they are provided in the input text. Provide only the complete p5.js code as output, with no additional text, explanations, comments, or markers. Separate code snippets: {input_text} """

full_code_validation_prompt = """ Review the following p5.js code, which is intended to display a text explanation using DOM elements. Analyze the code thoroughly for any syntax errors or logical issues, and ensure it is complete, fully functional, and ready to run without modifications. Strict requirements:

Use advanced techniques (such as a main container with CSS Flexbox/Grid via createDiv()) to ensure the display order of segments remains exactly as provided in the input text.
Output must maintain the original order of the provided code snippets, ensuring that the display order (e.g., text, visual, text) remains exactly as given, with no reordering.
Maintain the exact order of the given code snippets, integrating them sequentially without modifying their sequence.
Output only the final, fully working p5.js code.
Do not include any extra explanations, text, comments, or annotations.
Do not include any markdown code fences (e.g., p5.js or javascript).
Only print the p5.js code without any additional text, explanations, comments, or markers.(dont include ```javascript,```P5.js at all in the output need to perfect p5.js code only.)
Do not include any style tags or non-p5.js code. The generated code must strictly maintain the original order of the provided code snippets, ensuring that the display order remains exactly as given. The output must be complete and free of syntax errors. Generated code: {generated_code} """