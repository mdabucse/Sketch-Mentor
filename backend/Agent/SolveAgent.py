from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from SolveProblem.agent import GeminiP5JSGenerator
from visualAndSolve import MathProblemSolver
from SolveProblem.agent import FullcodeGenerator
import time
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProblemRequest(BaseModel):
    problem: str

class VisualizationResponse(BaseModel):
    generated_code: str

@app.post("/solve")
async def solve_problem(request: ProblemRequest):
    solver = MathProblemSolver()
    text_to_code = GeminiP5JSGenerator()
    full_code_generator = FullcodeGenerator()
    
    final_result = solver.solve_math_problem(request.problem)
    separate_code = ""
    for i, segment in enumerate(final_result.values()):
        if segment["type"] == "text":
            code = text_to_code.generate_p5js_code(segment["content"])
            separate_code += f"{i} th order/segment code\n"
            separate_code += code
        else:
            separate_code += f"{i} th order/segment code\n"
            separate_code += segment["content"]
    
    full_code = full_code_generator.generate_p5js_code(separate_code)
    # time.sleep(10)
    # full_code = """```javascript\nlet mainContainer;\n\nfunction setup() {\n  mainContainer = createDiv();\n  mainContainer.id('sketch-holder');\n\n  // 0 th order/segment code\n  let sketchHolder = 'sketch-holder';\n  let heading = createElement('h2', \"Let's break down the solution to the quadratic equation x² + 3x + 2 = 0 step by step.\");\n  heading.parent(mainContainer);\n  let stepsList = createElement('ol');\n  stepsList.parent(mainContainer);\n  let step1 = createElement('li');\n  step1.parent(stepsList);\n  let step1Heading = createElement('strong', \"Factor the quadratic expression:\");\n  step1Heading.parent(step1);\n  let step1Para1 = createP(\"Our goal is to rewrite the quadratic expression in the form (x + a)(x + b) = 0, where 'a' and 'b' are constants.  We need to find two numbers that multiply together to give us 'c' (the constant term, which is 2 in this case) and add up to give us 'b' (the coefficient of the x term, which is 3).\");\n  step1Para1.parent(step1);\n  let step1Para2 = createP(\"We can systematically list factor pairs of 2: 1 x 2, -1 x -2.\");\n  step1Para2.parent(step1);\n  let step1Para3 = createP(\"The pair that adds up to 3 is 1 and 2.\");\n  step1Para3.parent(step1);\n  let step1Para4 = createP(\"Therefore, we can rewrite the equation as (x + 1)(x + 2) = 0.\");\n  step1Para4.parent(step1);\n  let step1Para5 = createP(\"Think of it visually like a rectangle. The area of the rectangle is represented by our original quadratic x² + 3x + 2. We've now reshaped that rectangle into one with sides of length \");\n  let em1 = createElement('em', \"(x+1)\");\n  em1.parent(step1Para5);\n  step1Para5.html(step1Para5.html() + \" and \");\n  let em2 = createElement('em', \"(x+2)\");\n  em2.parent(step1Para5);\n  step1Para5.html(step1Para5.html() + \".\");\n  let step2 = createElement('li');\n  step2.parent(stepsList);\n  let step2Heading = createElement('strong', \"Apply the zero-product property:\");\n  step2Heading.parent(step2);\n  let step2Para1 = createP(\"This fundamental property of algebra states that if the product of two or more factors is zero, then at least one of those factors <em>must</em> be zero. In our factored equation (x + 1)(x + 2) = 0, the factors are (x + 1) and (x + 2).  So, either (x + 1) must equal 0, or (x + 2) must equal 0, or both could be zero.\");\n  step2Para1.parent(step2);\n  let step3 = createElement('li');\n  step3.parent(stepsList);\n  let step3Heading = createElement('strong', \"Solve for x in each case:\");\n  step3Heading.parent(step3);\n  let step3Para1 = createP(\"We now have two simpler equations to solve.\");\n  step3Para1.parent(step3);\n  let case1List = createElement('ul');\n  case1List.parent(step3);\n  let case1Item = createElement('li');\n  case1Item.parent(case1List);\n  let case1Heading = createElement('strong', \"Case 1: x + 1 = 0\");\n  case1Heading.parent(case1Item);\n  let case1Para = createP(\"To isolate x, we subtract 1 from both sides of the equation: x + 1 - 1 = 0 - 1, which simplifies to x = -1.\");\n  case1Para.parent(case1Item);\n  let case2Item = createElement('li');\n  case2Item.parent(case1List);\n  let case2Heading = createElement('strong', \"Case 2: x + 2 = 0\");\n  case2Heading.parent(case2Item);\n  let case2Para = createP(\"Similarly, we subtract 2 from both sides of the equation: x + 2 - 2 = 0 - 2, which simplifies to x = -2.\");\n  case2Para.parent(case2Item);\n  let step4 = createElement('li');\n  step4.parent(stepsList);\n  let step4Heading = createElement('strong', \"State the solutions:\");\n  step4Heading.parent(step4);\n  let step4Para1 = createP(\"We have found two values of x that satisfy the original equation: x = -1 and x = -2.  These are the solutions, also known as the roots or zeros, of the quadratic equation.\");\n  step4Para1.parent(step4);\n\n  // 1 th order/segment code\n  createCanvas(600, 400).parent(mainContainer); // Create a canvas and parent to mainContainer\n\n  // 2 th order/segment code\n  const sentence1 = createP(\"This visualization would show a parabola (the graph of \");\n  const code1 = createElement('code', 'y = x² + 3x + 2');\n  sentence1.child(code1);\n  sentence1.html(sentence1.html() + \") intersecting the x-axis at \");\n  const code2 = createElement('code', 'x = -1');\n  sentence1.child(code2);\n  sentence1.html(sentence1.html() + \" and \");\n  const code3 = createElement('code', 'x = -2');\n  sentence1.child(code3);\n  sentence1.html(sentence1.html() + \".\");\n  sentence1.parent(mainContainer);\n  const sentence2 = createP(\"These intersection points are the solutions we just found.\");\n  sentence2.parent(mainContainer);\n  const sentence3 = createP(\"The parabola opens upwards because the coefficient of \");\n  const code4 = createElement('code', 'x²');\n  sentence3.child(code4);\n  sentence3.html(sentence3.html() + \" is positive.\");\n  sentence3.parent(mainContainer);\n  const sentence4 = createP(\"The lowest point of the parabola (the vertex) would lie between \");\n  const code5 = createElement('code', '-1');\n  sentence4.child(code5);\n  sentence4.html(sentence4.html() + \" and \");\n  const code6 = createElement('code', '-2');\n  sentence4.child(code6);\n  sentence4.html(sentence4.html() + \".\");\n  sentence4.parent(mainContainer);\n}\n\nfunction draw() {\n  background(220); // Set background color\n\n  // --- Coordinate System Setup ---\n  const xMin = -5;   // Minimum x-value from DETAILS\n  const xMax = 2;    // Maximum x-value from DETAILS\n  const yMin = -2;   // Minimum y-value from DETAILS\n  const yMax = 10;  // Maximum y-value from DETAILS\n\n  const rangeX = xMax - xMin;\n  const rangeY = yMax - yMin;\n\n  const padding = 50; // Padding around the plot for labels and grid lines\n  const plotWidth = width - 2 * padding;\n  const plotHeight = height - 2 * padding;\n\n  // --- Coordinate Transformation Functions ---\n  function toScreenX(x) {\n    return map(x, xMin, xMax, padding, padding + plotWidth);\n  }\n\n  function toScreenY(y) {\n    return map(y, yMax, yMin, padding, padding + plotHeight); // Invert y-axis for screen coordinates\n  }\n\n  function toWorldX(screenX) {\n    return map(screenX, padding, padding + plotWidth, xMin, xMax);\n  }\n\n  function toWorldY(screenY) {\n    return map(screenY, padding, padding + plotHeight, yMax, yMin);\n  }\n\n  // --- Draw Grid Lines ---\n  stroke(200); // Light gray color for grid lines\n  strokeWeight(1);\n\n  // Vertical grid lines\n  for (let x = xMin; x <= xMax; x++) {\n    if (x !== 0) { // Avoid drawing grid line on the axis twice\n      const screenX = toScreenX(x);\n      line(screenX, padding, screenX, height - padding);\n    }\n  }\n\n  // Horizontal grid lines\n  for (let y = yMin; y <= yMax; y++) {\n    if (y !== 0) { // Avoid drawing grid line on the axis twice\n      const screenY = toScreenY(y);\n      line(padding, screenY, width - padding, screenY);\n    }\n  }\n\n  // --- Draw Axes ---\n  stroke(0); // Black color for axes\n  strokeWeight(2);\n\n  // x-axis\n  line(padding, toScreenY(0), width - padding, toScreenY(0));\n  // y-axis\n  line(toScreenX(0), height - padding, toScreenX(0), padding);\n\n  // --- Axis Labels ---\n  textSize(12);\n  fill(0);\n  textAlign(CENTER, TOP);\n  text('x', width - padding, toScreenY(0) + 5); // x-axis label\n  textAlign(RIGHT, CENTER);\n  text('y', toScreenX(0) - 5, padding); // y-axis label\n\n\n  // --- Plot the function y = x^2 + 3x + 2 ---\n  stroke(0, 0, 255); // Blue color for the function plot\n  strokeWeight(2);\n  noFill();\n\n  beginShape();\n  for (let x = xMin; x <= xMax; x += 0.01) { // Increment for smoother curve\n    let y = x*x + 3*x + 2; // Calculate y using the equation\n    vertex(toScreenX(x), toScreenY(y));\n  }\n  endShape();\n}\n```"""
    return  VisualizationResponse(generated_code=full_code)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
