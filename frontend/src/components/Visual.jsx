import React, { useState, useEffect, useRef } from 'react';
// import '../feature_css/visual.css';
import Header from './Header';

function Visual() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [activeVisualizationIndex, setActiveVisualizationIndex] = useState(null); // New state to track active visualization
  const canvasContainerRef = useRef(null);
  const messagesEndRef = useRef(null);

  // Auto-scroll to the bottom of the chat messages
  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [messages]);

  // Handle form submission to generate a new visualization
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (input.trim() === '') return;

    const userMessage = { text: input, sender: 'user', timestamp: new Date() };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await fetch('https://w4gw8kvg-8002.inc1.devtunnels.ms/generateVisual', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: input }),
      });

      if (!response.ok) throw new Error(`Server responded with ${response.status}`);

      const data = await response.json();
      const systemMessage = {
        text: 'Here is your visualization:',
        sender: 'system',
        visualization: data.generated_code,
        timestamp: new Date(),
      };

      // Update messages and set the new visualization as active
      setMessages((prev) => {
        const newMessages = [...prev, systemMessage];
        const newIndex = newMessages.length - 1;
        setActiveVisualizationIndex(newIndex);
        renderP5Visualization(systemMessage.visualization);
        return newMessages;
      });
    } catch (error) {
      console.error('Error generating visualization:', error);
      setMessages((prev) => [
        ...prev,
        { text: `Error: ${error.message}`, sender: 'system', timestamp: new Date() },
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Function to render p5.js visualization in an iframe
  const renderP5Visualization = (backendCode) => {
    if (canvasContainerRef.current) {
      canvasContainerRef.current.innerHTML = ''; // Clear previous content

      const iframe = document.createElement('iframe');
      iframe.width = '600';
      iframe.height = '400';
      iframe.style.border = 'none';
      canvasContainerRef.current.appendChild(iframe);

      const modifiedCode = backendCode.replace(
        /createCanvas\(([^)]+)\)/,
        "createCanvas($1).parent('p5-canvas-container')"
      );

      const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
      iframeDoc.open();
      iframeDoc.write(`
        <html>
        <head>
          <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.min.js"></script>
        </head>
        <body style="margin: 0;">
          <div id="p5-canvas-container"></div>
          <script>${modifiedCode}</script>
        </body>
        </html>
      `);
      iframeDoc.close();
    }
  };

  // Format timestamps for display
  const formatTime = (date) => {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className="app">
       <div> <Header /> </div>
      <div className="content">
        <div className="chat-container">
          <div className="messages">
            {messages.length === 0 && (
              <div className="welcome-message">
                <h2>Welcome to Visual Agent!</h2>
                <p>Describe the visualization you want, and I'll generate it for you.</p>
                <p>For example, try:</p>
                <ul>
                  <li>"Create a particle system with 100 particles"</li>
                  <li>"Show me a bar chart of monthly sales data"</li>
                  <li>"Generate a 3D rotating cube"</li>
                </ul>
              </div>
            )}
            {messages.map((message, index) => (
              <div
                key={index}
                className={`message ${message.sender === 'user' ? 'user-message' : 'system-message'} ${
                  message.visualization && index === activeVisualizationIndex ? 'active' : ''
                }`}
                onClick={() => {
                  if (message.visualization) {
                    setActiveVisualizationIndex(index);
                    renderP5Visualization(message.visualization);
                  }
                }}
                style={{ cursor: message.visualization ? 'pointer' : 'default' }} // Indicate clickability
              >
                <div className="message-header">
                  <span className="sender">{message.sender === 'user' ? 'You' : 'Visual Agent'}</span>
                  <span className="timestamp">{formatTime(message.timestamp)}</span>
                </div>
                <div className="message-content">
                  {message.text}
                  {message.visualization && (
                    <div className="code-preview">
                      <details>
                        <summary>View Generated Code</summary>
                        <pre><code>{message.visualization}</code></pre>
                      </details>
                    </div>
                  )}
                </div>
              </div>
            ))}
            {loading && (
              <div className="message system-message">
                <div className="message-content loading">
                  <div className="dot-flashing"></div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
          <form className="input-form" onSubmit={handleSubmit}>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Describe a visualization..."
              disabled={loading}
            />
            <button type="submit-btn-gen" disabled={loading || input.trim() === ''}>
              {loading ? 'Generating...' : 'Generate'}
            </button>
          </form>
        </div>
        <div className="canvas-container" ref={canvasContainerRef}>
          <div className="canvas-placeholder">
            <p>Your visualization will appear here</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Visual;