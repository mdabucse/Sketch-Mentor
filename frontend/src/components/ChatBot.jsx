import React, { useState, useEffect, useRef } from "react";
import { FaArrowUp } from "react-icons/fa6";
import { VscRobot } from "react-icons/vsc";
import { PiFinnTheHumanBold } from "react-icons/pi";
import axios from "axios";
import "../css/chatBot.css";

const ChatBot = () => {
  const [chats, setChats] = useState([]);
  const [messages, setMessages] = useState([]);
  const [inputText, setInputText] = useState("");
  const [chatName, setChatName] = useState("");
  const [currentChat, setCurrentChat] = useState(null);
  const [showMenu, setShowMenu] = useState(false);
  const [error, setError] = useState("");

  const API_BASE = " https://w4gw8kvg-5000.inc1.devtunnels.ms/";

  const chatEndRef = useRef(null); // Ref to track the latest message

  useEffect(() => {
    if (!currentChat && chats.length === 0) {
      fetchChatNames();
      startNewChatWithDefaultName();
    }
  }, [currentChat, chats]);

  // Fetch chat names from the API
  const fetchChatNames = async () => {
    try {
      const response = await axios.get(`${API_BASE}/chat_history`);
      const chatList = response.data.chat_names; // Accessing the chat names array
      setChats(chatList.map((chatTitle) => ({
        id: Date.now() + Math.random(), // Unique id for each chat, can be improved
        title: chatTitle,
        messages: [] // Initially empty messages array
      })));
    } catch (err) {
      console.error("Error fetching chat names:", err.message);
      setError("Failed to fetch chat names.");
    }
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]); // Scrolls to the latest message when messages update

  const startNewChatWithDefaultName = () => {
    const defaultChatName = `Chat ${chats.length + 1}`;
    const newChat = { id: Date.now(), title: defaultChatName, messages: [] };
    setChats([...chats, newChat]);
    setCurrentChat(newChat);
    setMessages([]);
  };

  const fetchChat = async () => {
    if (chatName.trim() === "") {
      setError("Please enter a chat name.");
      return;
    }
  
    try {
      const response = await axios.post(`${API_BASE}/chat_resume`, {
        chat_name: chatName,
      });
  
      if (!response.data.response || response.data.response.length === 0) {
        setError("No messages found for this chat.");
        return;
      }
  
      // Prepare fetched messages
      const fetchedMessages = response.data.response.flatMap(({ human, AI, timestamp }) => [
        human ? { text: human, type: "user", timestamp } : null,
        AI ? { text: AI, type: "bot", timestamp } : null,
      ]).filter(Boolean); // Remove null values
  
      setChats((prevChats) => {
        // Check if the chat already exists
        let existingChat = prevChats.find((chat) => chat.title === chatName);
        if (existingChat) {
          existingChat.messages = fetchedMessages;
          return [...prevChats];
        } else {
          const newChat = { id: Date.now(), title: chatName, messages: fetchedMessages };
          return [...prevChats, newChat];
        }
      });
  
      // Update current chat and messages
      setCurrentChat({ id: Date.now(), title: chatName, messages: fetchedMessages });
      setMessages(fetchedMessages);
      setError("");
    } catch (err) {
      console.error("Error fetching chat messages:", err.message);
      setError("Failed to fetch chat messages.");
    }
  };

  const sendMessage = async () => {
    if (inputText.trim() === "") return;

    const userMessage = inputText;
    setInputText("");

    try {
      let chat = currentChat;

      if (!chat) {
        const defaultChatName = `Chat ${chats.length + 1}`;
        const response = await axios.post(
          `${API_BASE}/chat_create`,
          { chat_name: defaultChatName },
          { headers: { "Content-Type": "application/json" } }
        );

        chat = { id: response.data.response, title: defaultChatName, messages: [] };
        setChats([...chats, chat]);
        setCurrentChat(chat);
      }

      const updatedMessages = [...(chat.messages || []), { text: userMessage, type: "user" }];
      setMessages(updatedMessages);

      const chatResponse = await axios.post(
        `${API_BASE}/chat`,
        { chat_name: chat.title, message: userMessage },
        { headers: { "Content-Type": "application/json" } }
      );

      const botReply = { text: chatResponse.data.response, type: "bot" };
      const finalMessages = [...updatedMessages, botReply];

      setMessages(finalMessages);
      setChats(chats.map((c) => (c.id === chat.id ? { ...c, messages: finalMessages } : c)));
      setCurrentChat({ ...chat, messages: finalMessages });

    } catch (err) {
      console.error("Error in sending message:", err.response ? err.response.data : err.message);
      setError(err.response?.data?.message || "Failed to send message.");
    }
  };

  // Handle chat selection from the chat history
  // const selectChat = (chat) => {
  //   setCurrentChat(chat);
  //   setMessages(chat.messages || []);  // Set the messages of the selected chat
  //   setChatName(chat.title);  // Update chat name input when selecting a chat
  //   setError("");  // Reset error
  // };

  const selectChat = async (chat) => {
    setCurrentChat(chat);
    setChatName(chat.title);  // Update chat name input when selecting a chat
    setError("");  // Reset error
  
    // If messages for the selected chat are already present, set them
    if (chat.messages.length > 0) {
      setMessages(chat.messages);
    } else {
      // Fetch messages for the selected chat from the backend
      try {
        const response = await axios.post(`${API_BASE}/chat_resume`, {
          chat_name: chat.title
        });
  
        // Assuming the response contains the messages
        const fetchedMessages = [];
  
        // Combine human and AI messages alternately
        for (let i = 0; i < response.data.response.length; i++) {
          const userMessage = response.data.response[i].human;
          const botMessage = response.data.response[i].AI;
  
          if (userMessage) {
            fetchedMessages.push({
              text: userMessage,
              type: "user",
              timestamp: response.data.response[i].timestamp
            });
          }
          
          if (botMessage) {
            fetchedMessages.push({
              text: botMessage,
              type: "bot",
              timestamp: response.data.response[i].timestamp
            });
          }
        }
  
        setMessages(fetchedMessages);
  
        // Update the current chat with the fetched messages
        const updatedChat = { ...chat, messages: fetchedMessages };
        setChats((prevChats) =>
          prevChats.map((prevChat) =>
            prevChat.id === chat.id ? updatedChat : prevChat
          )
        );
      } catch (err) {
        console.error("Error fetching chat messages:", err.message);
        setError("Failed to fetch chat messages.");
      }
    }
  };  
  
  
  const startNewChat = async () => {
    if (chatName.trim() === "") {
      setError("Chat name cannot be empty.");
      return;
    }

    if (chats.some((chat) => chat.title === chatName)) {
      setError("Chat name already exists.");
      return;
    }

    try {
      const response = await axios.post(
        `${API_BASE}/chat_create`,
        { chat_name: chatName },
        { headers: { "Content-Type": "application/json" } }
      );

      console.log("Chat Created:", response.data);

      const newChat = { id: response.data.response, title: chatName, messages: [] };
      setChats([...chats, newChat]);
      setCurrentChat(newChat);
      setMessages([]);
      setChatName("");
      setError("");
    } catch (err) {
      console.error("Error creating chat:", err.response ? err.response.data : err.message);
      setError(err.response?.data?.message || "Failed to create chat.");
    }
  };

  const handleChatNameChange = (newName) => {
    setError("");
    if (newName.trim() === "") {
      setError("Chat name cannot be empty.");
      return;
    }

    if (chats.some((chat) => chat.title === newName && chat.id !== currentChat.id)) {
      setError("Chat name already exists.");
      return;
    }

    if (currentChat) {
      const updatedChat = { ...currentChat, title: newName };
      const updatedChats = chats.map((chat) =>
        chat.id === currentChat.id ? updatedChat : chat
      );
      setChats(updatedChats);
      setCurrentChat(updatedChat);
      setError("");
    }
  };

  return (
    <div className="chat-bot">
      <div className="chat-container">
        <div className={`side-menu ${showMenu ? "open" : ""}`}>
          <button className="close-menu" onClick={() => setShowMenu(false)}>✖</button>

          <input
            type="text"
            className="chat-name-input"
            placeholder="Enter chat name..."
            value={chatName}
            onChange={(e) => setChatName(e.target.value)}
          />
          <button className="fetch-chat" onClick={fetchChat}>Fetch Chat</button>
          <button className="new-chat" onClick={startNewChat}>+ New Chat</button>

          {error && <div className="error-message">{error}</div>}

          <div className="chat-list">
            {chats.map((chat) => (
              <div key={chat.id} className="chat-item" onClick={() => selectChat(chat)}>
                {chat.title}
              </div>
            ))}
          </div>
        </div>

        <div className="chat-main">
          <button className="menu-button" onClick={() => setShowMenu(true)}>☰</button>

          <div className="chat-window">
          <div className="chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`chat-bubble ${msg.type}`}>
                {msg.type === "bot" && <VscRobot />} {/* Bot Icon */}
                {msg.type === "user" && <PiFinnTheHumanBold />} {/* User Icon */}
                <span>{msg.text}</span>
                {/* {msg.text} */}
              </div>
            ))}
            {/* Auto-scroll target */}
            <div ref={chatEndRef} />
          </div>
          </div>

          {currentChat && (
            <div className="edit-chat-name">
              <input
                type="text"
                value={currentChat.title}
                onChange={(e) => handleChatNameChange(e.target.value)}
              />
            </div>
          )}

          <div className="chat-input">
            <input
              type="text"
              placeholder="Type a message..."
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              onKeyPress={(e) => e.key === "Enter" && sendMessage()}
            />
            <button className="enter" onClick={sendMessage}><FaArrowUp /></button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;
