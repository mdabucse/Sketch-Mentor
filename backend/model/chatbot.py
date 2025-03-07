from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from pymongo import MongoClient
from datetime import datetime
from dotenv import load_dotenv
from model.conversation import conversation
import os
import json
load_dotenv()

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client.chatbot_db
chat_collection = db.chat_history

# # Gemini AI Model
# llm = ChatGoogleGenerativeAI(model="gemini-pro", google_api_key=os.getenv("GEMINI_API_KEY"))

# # Memory to store last 3 conversations
# memory = ConversationBufferMemory(k=3)
# conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

def create_or_get_chat(chat_name):
    """Create a new chat session if it doesn't exist, else return existing session."""
    session_data = chat_collection.find_one({"chat_name": chat_name})
    if session_data:
        return session_data["session_id"]
    session_id = str(datetime.utcnow().timestamp())
    chat_collection.insert_one({
        "session_id": session_id,
        "chat_name": chat_name,
        "messages": [],
        "timestamp": datetime.utcnow(),
        "ended": False
    })
    return ("Chat Created Successfully",session_id)

# def load_past_conversations(chat_name):
#     """Load the last 3 messages from a given chat into memory."""
#     session_data = chat_collection.find_one({"chat_name": chat_name})
#     if session_data and "messages" in session_data:
#         for msg in session_data["messages"][-3:]:  # Load last 3 messages
#             memory.chat_memory.add_user_message(msg["human"])
#             memory.chat_memory.add_ai_message(msg["AI"])

def store_chat_in_mongo(chat_name, user_message, ai_message):
    """Store the conversation messages in MongoDB."""
    chat_collection.update_one(
        {"chat_name": chat_name},
        {
            "$push": {
                "messages": {
                    "human": user_message,
                    "AI": ai_message,
                    "timestamp": datetime.utcnow()
                }
            },
            "$set": {"timestamp": datetime.utcnow()}
        },
        upsert=True
    )

def end_chat_session(chat_name):
    """Mark the session as ended and store conversation in paired {human, AI} format."""
    session_data = chat_collection.find_one({"chat_name": chat_name})
    if session_data and "messages" in session_data:
        chat_pairs = [
            {"human": msg["human"], "AI": msg["AI"]}
            for msg in session_data["messages"]
        ]
        chat_collection.update_one(
            {"chat_name": chat_name},
            {
                "$set": {
                    "chat_pairs": chat_pairs,
                    "ended": True,
                    "timestamp": datetime.utcnow()
                }
            }
        )

def resume_chat_session(chat_name):
    """Fetch all past messages from a session."""
    session_data = chat_collection.find_one({"chat_name": chat_name})
    return session_data["messages"] if session_data and "messages" in session_data else []

def fetch_all_chat_names():
    chat_names = [chat["chat_name"] for chat in chat_collection.find({}, {"chat_name": 1, "_id": 0})]
    
    return chat_names

def main(chat_name,user_message):
    # create_or_get_chat(chat_name)
    # if end_session == True:
    #     end_chat_session(chat_name)
    #     print("Chat session ended.")
    
    ai_response = conversation(user_message)
    store_chat_in_mongo(chat_name, user_message, ai_response)
    return ai_response