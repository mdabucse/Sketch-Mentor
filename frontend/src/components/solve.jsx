import React, { useState, useRef, useEffect } from 'react';
// import "../feature_css/solve.css";
import Header from './Header';

function Solve() {
  const [input, setInput] = useState(''); // State for user input
  const [loading, setLoading] = useState(false); // State for loading status
  const [darkMode, setDarkMode] = useState(false); // State for dark mode
  const [copied, setCopied] = useState(false); // State for copy indicator
  const canvasContainerRef = useRef(null); // Reference to the canvas container
  const inputRef = useRef(null); // Reference to the input field
  
  // Example math problems for quick selection
  const examples = [
    "x² + 3x + 2 = 0",
    "sin(x) * cos(x)",
    "y = 2x² - 4x + 7",
    "e^x - log(x)",
    "sqrt(x²+y²) = 5"
  ];

// Add this function to your Solve component to create and display the loading animation
const showLoadingAnimation = () => {
  if (canvasContainerRef.current) {
    // Clear the container first
    canvasContainerRef.current.innerHTML = '';
    
    // Create loading container
    const loadingContainer = document.createElement('div');
    loadingContainer.className = 'math-loading-container';
    
    // Create header for the loading animation
    const loadingHeader = document.createElement('div');
    loadingHeader.className = 'loading-header';
    loadingHeader.innerHTML = '<h3>Processing Math Visualization</h3>';
    loadingContainer.appendChild(loadingHeader);
    
    // Agent steps with their descriptions
    const agents = [
      { name: 'Prompt Analysis', description: 'Understanding mathematical expression' },
      { name: 'Math Verification', description: 'Validating mathematical correctness' },
      { name: 'Visualization Spec', description: 'Designing visual representation' },
      { name: 'Code Structure', description: 'Planning visualization architecture' },
      { name: 'Code Generation', description: 'Creating visual implementation' },
      { name: 'Safety Sanitization', description: 'Ensuring safe execution' },
      { name: 'Validation Consensus', description: 'Finalizing visualization' }
    ];
    
    // Create agent steps container
    const stepsContainer = document.createElement('div');
    stepsContainer.className = 'agent-steps-container';
    
    // Create and append each agent step
    agents.forEach((agent, index) => {
      const stepElement = document.createElement('div');
      stepElement.className = 'agent-step';
      stepElement.dataset.step = index;
      
      const iconContainer = document.createElement('div');
      iconContainer.className = 'step-icon';
      const iconInner = document.createElement('div');
      iconInner.className = 'step-icon-inner';
      iconContainer.appendChild(iconInner);
      
      const contentContainer = document.createElement('div');
      contentContainer.className = 'step-content';
      
      const nameElement = document.createElement('div');
      nameElement.className = 'step-name';
      nameElement.textContent = agent.name;
      
      const descElement = document.createElement('div');
      descElement.className = 'step-description';
      descElement.textContent = agent.description;
      
      contentContainer.appendChild(nameElement);
      contentContainer.appendChild(descElement);
      
      stepElement.appendChild(iconContainer);
      stepElement.appendChild(contentContainer);
      stepsContainer.appendChild(stepElement);
    });
    
    loadingContainer.appendChild(stepsContainer);
    
    // Create mathematical symbols that float in the background
    const mathSymbolsContainer = document.createElement('div');
    mathSymbolsContainer.className = 'math-symbols-background';
    
    const symbols = ['∫', '∑', 'π', '∞', 'Δ', '√', '∂', 'θ', 'λ', 'Ω', '+', '−', '×', '÷', '='];
    for (let i = 0; i < 15; i++) {
      const symbol = document.createElement('div');
      symbol.className = 'floating-math-symbol';
      symbol.textContent = symbols[Math.floor(Math.random() * symbols.length)];
      symbol.style.left = `${Math.random() * 100}%`;
      symbol.style.animationDelay = `${Math.random() * 5}s`;
      symbol.style.animationDuration = `${5 + Math.random() * 10}s`;
      symbol.style.opacity = 0.1 + Math.random() * 0.3;
      symbol.style.fontSize = `${1 + Math.random() * 2}rem`;
      mathSymbolsContainer.appendChild(symbol);
    }
    
    loadingContainer.appendChild(mathSymbolsContainer);
    
    // Create pulsating equation display
    const equationDisplay = document.createElement('div');
    equationDisplay.className = 'equation-display';
    equationDisplay.textContent = input; // Show the current equation
    loadingContainer.appendChild(equationDisplay);
    
    canvasContainerRef.current.appendChild(loadingContainer);
    
    // Start animation sequence
    startLoadingSequence();
  }
};

// Function to animate through the agent steps
const startLoadingSequence = () => {
  const steps = document.querySelectorAll('.agent-step');
  let currentStep = 0;
  
  // Activate first step immediately
  if (steps.length > 0) {
    steps[0].classList.add('active');
  }
  
  // Function to activate a step
  const activateStep = (stepIndex) => {
    if (stepIndex < steps.length) {
      steps[stepIndex].classList.add('active');
      
      // Add "working" class to show it's in progress
      steps[stepIndex].classList.add('working');
      
      // After a delay, mark it as completed
      setTimeout(() => {
        steps[stepIndex].classList.remove('working');
        steps[stepIndex].classList.add('completed');
        
        // Move to next step if not the last one
        if (stepIndex < steps.length - 1) {
          currentStep++;
          activateStep(currentStep);
        }
      }, 800 + Math.random() * 1200); // Random time between 0.8-2 seconds for each step
    }
  };
  
  // Start the sequence
  activateStep(currentStep);
};

// Modify the handleSubmit function to use the loading animation
const handleSubmit = async (e) => {
  e.preventDefault();
  if (input.trim() === '') return;

  setLoading(true);
  showLoadingAnimation(); // Show our new loading animation

  try {
    // Send POST request to the /solve endpoint
    const response = await fetch('https://w4gw8kvg-8000.inc1.devtunnels.ms/solve', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problem: input }),
    });

    if (!response.ok) throw new Error(`Server responded with ${response.status}`);

    const data = await response.json();
    // Extract P5.js code from the response
    const code = extractCodeFromResponse(data.generated_code || data.final_explanation);
    renderP5Visualization(code); // Render the visualization
  } catch (error) {
    console.error('Error solving problem:', error);
    // Show error message inside canvas container
    if (canvasContainerRef.current) {
      canvasContainerRef.current.innerHTML = `
        <div class="error-message">
          <p>Oops! Something went wrong while processing your request.</p>
          <p>Error: ${error.message}</p>
          <p>Please try again with a different equation.</p>
        </div>
      `;
    }
  } finally {
    setLoading(false);
  }
};

  // Extract P5.js code from the response, removing triple backticks if present
  const extractCodeFromResponse = (code) => {
    if (!code) return '';
    const match = code.match(/```([\s\S]*?)```/);
    return match ? match[1].trim() : code.trim(); // Fallback to raw text if no backticks
  };

  // Render the P5.js visualization in an iframe with increased height
  const renderP5Visualization = (Code) => {
    const extractCodeFromResponse = (Code) =>
      Code.replace("javascript", "").trim();
    const backendCode = extractCodeFromResponse(Code);
    console.log(backendCode);
    if (canvasContainerRef.current) {
      canvasContainerRef.current.innerHTML = ''; // Clear previous visualization
      
      // Add copy button to container
      const copyButton = document.createElement('button');
      copyButton.className = 'copy-btn';
      copyButton.innerHTML = '<i>📋</i>';
      copyButton.title = 'Copy visualization code';
      copyButton.onclick = () => {
        navigator.clipboard.writeText(backendCode);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
        copyButton.innerHTML = '<i>✓</i>';
        setTimeout(() => {
          copyButton.innerHTML = '<i>📋</i>';
        }, 2000);
      };
      canvasContainerRef.current.appendChild(copyButton);

      const iframe = document.createElement('iframe');
      iframe.width = '100%'; // Width to accommodate the canvas
      iframe.height = '1000'; // Increased height to fit both text and canvas
      iframe.style.border = 'none'; // Clean appearance
      canvasContainerRef.current.appendChild(iframe);

      // Modify code to parent the canvas if not already specified
      const modifiedCode = backendCode.includes('.parent(')
        ? backendCode
        : backendCode.replace(
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
  
  // Insert math symbol into input at cursor position
  const insertSymbol = (symbol) => {
    if (inputRef.current) {
      const cursorPosition = inputRef.current.selectionStart;
      const textBefore = input.substring(0, cursorPosition);
      const textAfter = input.substring(cursorPosition);
      setInput(textBefore + symbol + textAfter);
      
      // Focus back to input and set cursor position after inserted symbol
      setTimeout(() => {
        inputRef.current.focus();
        inputRef.current.setSelectionRange(
          cursorPosition + symbol.length,
          cursorPosition + symbol.length
        );
      }, 10);
    }
  };
  
  // Toggle dark mode
  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    document.body.classList.toggle('dark-mode');
  };
  
  // Create floating math symbols as background decoration
  useEffect(() => {
    const symbols = ['∫', '∑', 'π', '∞', 'Δ', '√', '∂', 'θ', 'λ', 'Ω'];
    const container = document.createElement('div');
    container.className = 'floating-math-symbols';
    
    for (let i = 0; i < 20; i++) {
      const symbol = document.createElement('div');
      symbol.className = 'floating-symbol';
      symbol.textContent = symbols[Math.floor(Math.random() * symbols.length)];
      
      // Set random positions and animation variables
      const randomX = Math.random() * 100;
      const randomSize = 1 + Math.random() * 2;
      symbol.style.cssText = `
        left: ${randomX}%;
        font-size: ${randomSize}rem;
        --random: ${Math.random()};
      `;
      
      container.appendChild(symbol);
    }
    
    document.querySelector('.solve-app').appendChild(container);
    
    return () => {
      if (document.querySelector('.floating-math-symbols')) {
        document.querySelector('.floating-math-symbols').remove();
      }
    };
  }, []);

  return (
    <div>
        <div> <Header />  </div>
    <div className={`solve-app ${darkMode ? 'dark-mode' : ''}`}>
      <div className="theme-toggle" onClick={toggleDarkMode} title="Toggle dark/light mode">
        <div className="theme-toggle-icon"></div>
      </div>
      
      <h1>Mathematical Visualizer</h1>
      
      <div className="example-suggestions">
        {examples.map((example, index) => (
          <div 
            key={index} 
            className="example-chip"
            onClick={() => {
              setInput(example);
              inputRef.current.focus();
            }}
          >
            {example}
          </div>
        ))}
      </div>
      
      <form className="input-form" onSubmit={handleSubmit}>
        <input
          ref={inputRef}
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Enter a mathematical expression..."
          disabled={loading}
        />
        
        <div className="math-symbols">
          <div className="math-symbol" onClick={() => insertSymbol('²')}>x²</div>
          <div className="math-symbol" onClick={() => insertSymbol('√')}>√</div>
          <div className="math-symbol" onClick={() => insertSymbol('π')}>π</div>
          <div className="math-symbol" onClick={() => insertSymbol('∫')}>∫</div>
        </div>
        
        <button type="submit" disabled={loading || input.trim() === ''}>
          {loading ? (
            <span className="loading-indicator">Calculating</span>
          ) : (
            'Visualize'
          )}
        </button>
      </form>
      
      <div className="canvas-container" ref={canvasContainerRef}>
        {!loading && !canvasContainerRef.current?.innerHTML && (
          <div className="empty-state">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1" strokeLinecap="round" strokeLinejoin="round">
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="8" x2="12" y2="16"></line>
              <line x1="8" y1="12" x2="16" y2="12"></line>
            </svg>
            <p>Enter a mathematical expression above or select an example to see its visualization</p>
          </div>
        )}
      </div>
    </div>
    </div>
  );
}

export default Solve;