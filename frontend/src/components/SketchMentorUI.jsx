import React, { useState } from 'react';
import { useNavigate } from "react-router-dom";
import "../css/SketchMentorUI.css";
import { LiaFileVideoSolid } from "react-icons/lia";
import { FaLink, FaChartPie, FaPuzzlePiece, FaYoutube } from "react-icons/fa";
import Header from './Header';

const SketchMentorUI = () => {
  const [videoUrl, setVideoUrl] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  // Function to validate YouTube URL
  const isValidYouTubeUrl = (url) => {
    const pattern =
      /^(https?:\/\/)?(www\.)?(youtube\.com\/watch\?v=|youtu\.be\/)[a-zA-Z0-9_-]+$/;
    return pattern.test(url);
  };

  const handleSubmit = async () => {
    // if (!isValidYouTubeUrl(videoUrl)) {
    //   setError("Invalid YouTube URL. Please enter a valid link.");
    //   return;
    // }

    setLoading(true); 

    try {
      const response = await fetch("https://w4gw8kvg-5000.inc1.devtunnels.ms/transcript", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ video_ids: videoUrl }), // Sending video URL
      });

      if (!response.ok) {
        throw new Error("Failed to fetch transcript");
      }

      const data = await response.json();
      console.log("Transcript Response:", data); // Debugging purposes

      // Navigate to Home page with videoUrl and transcript data
      navigate("/home", { state: { videoUrl, transcript: data } });

    } catch (error) {
      console.error("Error fetching transcript:", error);
      setError("Failed to fetch transcript. Please try again.");
    } finally {
        setLoading(false); // Stop loading animation
    }
  
  };

  return (
    <div className="container2">
      {/* Header */}
      {/* <header className="header2">
        <div className="logo">SKETCH MENTOR</div>
        <a href="#" className="login">Login</a>
      </header> */}
      <div> <Header /> </div>

      {/* Hero Section */}
      <div className="hero">
        <h1>
          <strong>Top Features of Sketch Mentor</strong> <br />
        </h1>
      </div>

      {/* Interactive Blocks */}
      <div className="blocks">
        {/* Enter Link Block */}
        <div className='div1'>
          <div className="block link-block">
            <FaYoutube className="block-icon1" />
            <input
              type="text"
              placeholder="Enter a video URL"
              value={videoUrl}
              onChange={(e) => {
                setVideoUrl(e.target.value);
                setError(""); // Clear error on change
              }}
              className="video-input1"
            />
            {/* <button className="proceed-btn1" onClick={handleSubmit}>Proceed</button> */}
            <button onClick={handleSubmit} className="proceed-btn1" disabled={loading}>
            {loading ? <div className="spinner"></div> : "Proceed"}
            </button>
            {error && <p className="error">{error}</p>}
          </div>
        </div>

        {/* Other Feature Blocks */}
        <div className='div2'>
          <div className='div2-part1'>
            <div className="block1" onClick={() => navigate("/math-visualization")}>
              <LiaFileVideoSolid className="block-icon" />
              <p>Video Generator</p>
            </div>
          </div>

          <div className='div2-part2'>
            <div className="block2" onClick={() => navigate("/Visual")}>
              <FaChartPie className="block-icon" />
              <p>Visualizer</p>
            </div>

            <div className="block2" onClick={() => navigate("/solve")}>
              <FaPuzzlePiece className="block-icon" />
              <p>Interactive Solver</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SketchMentorUI;
