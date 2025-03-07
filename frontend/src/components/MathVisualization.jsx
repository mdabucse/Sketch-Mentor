import React, { useState, useRef, useEffect } from 'react';
// import '../feature_css/MathVisual.css';
import { FaPlay, FaRedo, FaInfoCircle } from 'react-icons/fa';
import { 
  BsGraphUp, 
  BsCheck2Circle, 
  BsCode, 
  BsPencilSquare, 
  BsMegaphone,
  BsShieldCheck,
  BsClipboardCheck
} from 'react-icons/bs';
import Header from './Header';

const MathVisualization = () => {
  const [problem, setProblem] = useState('');
  const [videoPath, setVideoPath] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [currentStage, setCurrentStage] = useState(0);
  const videoRef = useRef(null);
  const [showTip, setShowTip] = useState(false);

  // Agent pipeline stages
  const stages = [
    { name: "Prompt Analysis", icon: <BsPencilSquare />, description: "Analyzing your math problem" },
    { name: "Math Verification", icon: <BsCheck2Circle />, description: "Verifying mathematical correctness" },
    { name: "Visualization Spec", icon: <BsGraphUp />, description: "Designing visualization approach" },
    { name: "Voice Generation", icon: <BsMegaphone />, description: "Preparing narration script" },
    { name: "Code Structure", icon: <BsCode />, description: "Designing code architecture" },
    { name: "Code Generation", icon: <BsCode />, description: "Generating Manim visualization code" },
    { name: "Safety Checks", icon: <BsShieldCheck />, description: "Running safety checks" },
    { name: "Validation", icon: <BsClipboardCheck />, description: "Final validation" },
    { name: "Rendering", icon: <FaPlay />, description: "Rendering your video" }
  ];

  // Example math problems for inspiration
  const exampleProblems = [
    "Visualize the Pythagorean theorem with a right triangle",
    "Show the geometric interpretation of complex number multiplication",
    "Demonstrate the chain rule in calculus with a simple function",
    "Visualize how the quadratic formula solves ax² + bx + c = 0",
    "Show the relationship between sine and cosine on the unit circle"
  ];

  // Fix video playback when path changes
  useEffect(() => {
    if (videoRef.current && videoPath) {
      // Force reload the video element when path changes
      videoRef.current.load();
    }
  }, [videoPath]);

  const simulateAgentPipeline = async () => {
    // This simulates the agent pipeline process with delays
    for (let i = 0; i < stages.length; i++) {
      setCurrentStage(i);
      // Random delay between 1-3 seconds for each stage
      await new Promise(resolve => setTimeout(resolve, 1000 + Math.random() * 2000));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!problem.trim()) {
      setError('Please enter a math problem');
      return;
    }

    setLoading(true);
    setError('');
    setVideoPath('');
    setCurrentStage(0);

    try {
      // Start the agent pipeline simulation
      const pipelinePromise = simulateAgentPipeline();

      const response = await fetch('https://w4gw8kvg-8001.inc1.devtunnels.ms/videoGeneration', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ problem }),
      });
      
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Server error occurred');
      }
      
      const data = await response.json();
      
      // Make sure to use the full URL for the video path
      setVideoPath(data.video_path);
      
      // Wait for the pipeline simulation to complete
      await pipelinePromise;
      
    } catch (err) {
      console.error("Error during video generation:", err);
      setError(err.message || 'An error occurred during video generation');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setProblem('');
    setVideoPath('');
    setError('');
    setLoading(false);
  };

  const insertExample = (example) => {
    setProblem(example);
  };

  const handlePlayVideo = () => {
    if (videoRef.current) {
      // Check if video is loaded before playing
      if (videoRef.current.readyState >= 2) {
        videoRef.current.play().catch(err => {
          console.error("Error playing video:", err);
          setError("Could not play video. Please try again.");
        });
      } else {
        setError("Video is not ready to play yet. Please wait a moment.");
      }
    }
  };

  return (
    <div>
        <div> <Header /> </div>
    <div className="math-viz-container">
      <div className="math-viz-header">
        <h1>Mathematical Visualization Generator</h1>
        <p>Enter a mathematical concept or problem to create a dynamic visualization</p>
      </div>

      <div className="math-viz-content">
        <div className="math-viz-input-section">
          <form onSubmit={handleSubmit}>
            <div className="input-wrapper">
              <textarea
                value={problem}
                onChange={(e) => setProblem(e.target.value)}
                placeholder="Describe a mathematical concept or problem (e.g., 'Visualize the Pythagorean theorem')"
                disabled={loading}
                rows={5}
                className="math-input"
              />
              <div className="info-icon" onMouseEnter={() => setShowTip(true)} onMouseLeave={() => setShowTip(false)}>
                <FaInfoCircle />
                {showTip && (
                  <div className="tooltip">
                    Be specific about what aspects you want visualized. Include any parameters or constraints.
                  </div>
                )}
              </div>
            </div>

            <div className="examples-section">
              <p>Try one of these examples:</p>
              <div className="example-chips">
                {exampleProblems.map((ex, index) => (
                  <button 
                    type="button" 
                    key={index} 
                    className="example-chip"
                    onClick={() => insertExample(ex)}
                    disabled={loading}
                  >
                    {ex}
                  </button>
                ))}
              </div>
            </div>

            <div className="button-group">
              <button type="submit" className="submit-btn" disabled={loading}>
                Generate Visualization
              </button>
              <button type="button" className="reset-btn" onClick={handleReset} disabled={loading}>
                <FaRedo /> Reset
              </button>
            </div>
          </form>

          {error && <div className="error-message">{error}</div>}
        </div>

        {loading && (
          <div className="pipeline-visualization">
            <h3>Generation in Progress</h3>
            <div className="pipeline-stages">
              {stages.map((stage, index) => (
                <div 
                  key={index} 
                  className={`pipeline-stage ${index === currentStage ? 'active' : ''} ${index < currentStage ? 'completed' : ''}`}
                >
                  <div className="stage-icon">
                    {stage.icon}
                  </div>
                  <div className="stage-info">
                    <div className="stage-name">{stage.name}</div>
                    {index === currentStage && (
                      <div className="stage-description">{stage.description}</div>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {videoPath && !loading && (
          <div className="video-result">
            <h3>Visualization Result</h3>
            <div className="video-container">
              <video 
                ref={videoRef} 
                controls 
                className="result-video"
                src={videoPath}
                onError={(e) => {
                  console.error("Video error:", e);
                  setError("Error loading video. The file might not be available yet or the path is incorrect.");
                }}
              >
                Your browser does not support the video tag.
              </video>
            </div>
            <div className="video-controls">
              <button 
                className="control-btn play-btn" 
                onClick={handlePlayVideo}
              >
                <FaPlay /> Play
              </button>
            </div>
            <div className="video-path-info">
              <p className="video-path-text">Video path: {videoPath}</p>
            </div>
          </div>
        )}
      </div>

      <div className="math-viz-footer">
        <p>Powered by Team Techiee Hackers</p>
      </div>
    </div>
    </div>
  );
};

export default MathVisualization;