from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import json
from dotenv import load_dotenv
from model.rag import rag_main

load_dotenv()

def conversation(user_message):
    transcript_file = r"A:\Projects\Edu_Pro\backend\data\single.json"
    content = rag_main(user_message)
    print("The rag provided content is",content)
    if user_message.lower() in ["hi", "hii", "hello", "hey"]:
        print("If working")
        prompt = f"""
        You are an expert in problem-solving in Mathematics.
        When a user greets you, respond with:
        "Hello! What can I assist you with today? Here are some example questions you can ask me:"
        {content}
        """
    # if not content or "Sorry" in content:
    #     content = "Example questions are currently unavailable. Please ask your question directly."

    else:
        print("Else Working")
        prompt = f"""
        You are an expert in problem-solving in Mathematics.
        Based on the following extracted content, generate the most relevant answer to the user's question.

        User's question: "{user_message}"

        Relevant content:
        {content}

        Provide a concise and helpful response.
        """
    print("The prompt is",prompt)
    llm = ChatGoogleGenerativeAI(model="models/gemini-1.5-pro-001", google_api_key=os.getenv("GEMINI_API_KEY"))
    ai_response = llm.predict(prompt)
    return ai_response