# AI Math Tutor 🔢🤖

## Overview
The current OLabs platform lacks AI-driven mathematical problem-solving, making it difficult for students to get instant solutions. There is no real-time equation recognition or automated system to solve handwritten math problems. Additionally, students cannot extract transcripts from educational videos and procedures to receive AI-generated answers, making it harder to understand complex equations step by step.

## Features

### CANVAS AI
The mathematics-focused canvas allows users to write equations and draw diagrams, enabling AI to recognize and solve them in real-time. It provides instant, step-by-step solutions, making complex problem-solving easier and more interactive for students.

### VIDEO TRANSCRIBER
The video transcriber converts audio from videos into text using the OpenAI Whisper model. This enables accurate transcription, allowing students to access and search educational content more effectively.

### RAG CHATBOT
The RAG-based chatbot processes the transcripts to provide accurate answers. It enables students to ask questions related to the video and receive context-aware responses, enhancing their learning experience.

## How It Enhances OLabs
- Adds AI-powered problem-solving to OLabs.
- Improves mathematics learning through real-time equation solving.
- Helps students understand complex equations step-by-step.
- Makes educational videos more interactive with video transcript-based Q&A.
- Boosts engagement & accessibility for students using OLabs.

## Innovation
- AI-powered equation recognition for handwritten/math input.
- Multilingual support for transcripts & chatbot responses.
- Works on any device (web & mobile) for flexible learning.

## Tech Stack
- Gemini
- OpenAI Whisper
- Langchain
- Flask
- React
- MongoDB

## Code Structure

### Frontend
```
components/
  - Canvas.jsx
  - ChatBot.jsx
  - Transcript.jsx
  - VideoPlayer.jsx

styles/
  - canvasStyles.css
  - chatBot.css
  - homepage.css
  - transcript.css
  - App.css

- App.jsx
- Home.jsx
- index.css
- main.jsx
```

### Backend
```
canvas_backend/
  apps/calculator/
    - route.py
    - utils.py
  
  - .gitignore
  - app.py
  - constants.py
  - main.py
  - requirements.txt
  - schema.py

  data/
    - chat_history.json
    - multi.json
    - single.json

  model/
    - Transcription_19 TOXIC Tech F...
    - audio.mp3

  - chatbot.py
  - conversation.py
  - flowchart.py
  - rag.py
  - transcript.json
  - try.html
  - try.py
  - video_to_transcribe.py
  - youtube_transcriber.py
  - audio.mp3
  - backend.py
  - faiss_index.index
```

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/your-repo/ai-math-tutor.git
   ```
2. Navigate to the project directory:
   ```sh
   cd ai-math-tutor
   ```
3. Install dependencies for the frontend:
   ```sh
   cd frontend
   npm install
   ```
4. Install dependencies for the backend:
   ```sh
   cd backend
   pip install -r requirements.txt
   ```
5. Run the frontend:
   ```sh
   npm start
   ```
6. Run the backend:
   ```sh
   python app.py
   ```
## Prototype

https://github.com/user-attachments/assets/818f23ff-fbe3-4b5f-9101-e68b1992cfbe

