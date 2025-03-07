# Agentic Multi-Modal Visualization & Math Problem Solving System

This repository hosts three FastAPI-based microservices that work together to solve math problems, generate interactive visualizations, and produce video visualizations. The services integrate advanced AI and rendering modules to help educators, students, and developers understand math concepts through dynamic visualizations and interactive code.

## Overview

This system consists of three microservices:

1. *Video Generation Service* – Generates video visualizations (using Manim) for math problems.
2. *Visualization Generation Service* – Creates interactive visualization code (p5.js) based on user prompts.
3. *Math Problem Solver Service* – Solves math problems and generates step-by-step p5.js visualization code segments.

Each service runs on its own FastAPI application, making it easy to maintain and scale individual components.

## Services Overview

- **Video Generation Service (videoModel)**
  - *Port:* 8001
  - *Key Endpoint:* /videoGeneration
  - *Additional Endpoint:* /health (for health checks)
  - *Description:* Accepts a math problem and generates a Manim video that visually explains the solution process.

- **Visualization Generation Service (visualAgent)**
  - *Port:* 8002
  - *Key Endpoint:* /generateVisual
  - *Description:* Accepts a prompt and returns generated p5.js code for interactive visualizations.

- **Math Problem Solver Service (SolveAgent)**
  - *Port:* (default, when started via uvicorn without specifying a port, or can be set in the command)
  - *Key Endpoint:* /solve
  - *Description:* Processes math problems by solving and breaking them into segments, then generates comprehensive p5.js code to visualize the solution.

## Getting Started

### Prerequisites

- *Python 3.8+*
- *pip* (Python package manager)
- *Virtual Environment* (recommended for dependency isolation)
- *Manim* (for the video generation service – see [Manim Documentation](https://docs.manim.community/))
- Additional dependencies are listed in the requirements.txt file.

### Installation

1. *Clone the Repository:*
   ```bash
   git clone https://github.com/yourusername/agentic-visualization-system.git
   cd Agent
