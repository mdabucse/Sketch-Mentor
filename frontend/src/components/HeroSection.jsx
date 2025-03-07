import React from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate
import '../css/HeroSection.css';

function HeroSection() {

  const navigate = useNavigate();
  
  const handleGetStartedClick = () => {
    navigate('/sketch-mentor'); // Navigate to the SketchMentorUI route
  };

    return (
      <section className="hero-section">
        <div className="grid-background"></div>
        
        <div className="hero-icons">
          {/* <div className="paper-plane">
            <svg width="60" height="60" viewBox="0 0 60 60" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M5 5L30 30L55 5" stroke="black" strokeWidth="2" />
              <path d="M5 5L30 55L55 5" stroke="black" strokeWidth="2" />
            </svg>
          </div> */}
          
          {/* <div className="formula">
            <span>E=mc²</span>
          </div> */}
          
          <div className="grade-paper">
            {/* <svg width="40" height="50" viewBox="0 0 40 50" fill="none" xmlns="http://www.w3.org/2000/svg">
              <rect x="5" y="5" width="30" height="40" fill="white" stroke="black" />
              <text x="15" y="25" fontFamily="Arial" fontSize="16" fill="black">A+</text>
              <line x1="10" y1="30" x2="30" y2="30" stroke="black" strokeWidth="1" />
              <line x1="10" y1="35" x2="25" y2="35" stroke="black" strokeWidth="1" />
            </svg> */}
          </div>
          
          <div className="atom">
            {/* <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="20" cy="20" r="8" stroke="black" strokeWidth="1" fill="none" />
              <ellipse cx="20" cy="20" rx="18" ry="10" stroke="black" strokeWidth="1" fill="none" transform="rotate(60 20 20)" />
              <ellipse cx="20" cy="20" rx="18" ry="10" stroke="black" strokeWidth="1" fill="none" transform="rotate(-60 20 20)" />
              <circle cx="20" cy="20" r="2" fill="black" />
            </svg> */}
          </div>
          
          <div className="dinosaur">
            {/* <svg width="60" height="40" viewBox="0 0 60 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M50 25C45 25 40 20 40 15C40 10 45 5 50 5C55 5 60 10 60 15C60 20 55 25 50 25Z" stroke="black" strokeWidth="1" fill="none" />
              <path d="M40 15L20 15C15 15 10 20 10 25C10 30 15 35 20 35L40 35" stroke="black" strokeWidth="1" fill="none" />
              <path d="M40 35L50 25" stroke="black" strokeWidth="1" />
              <path d="M50 5L55 1M53 5L57 3M55 8L58 7" stroke="black" strokeWidth="1" />
            </svg> */}
          </div>
        </div>
        
        <div className="hero-content">
          <h1>Bring your learning to life.</h1>
          <p>Enhance your education with AI-Powered Education</p>
          
          <div className="cta-container">
            <button className="get-started-btn"  onClick={handleGetStartedClick}>
              Get Started
              <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M8 1L15 8L8 15" stroke="currentColor" strokeWidth="2" />
                <path d="M15 8H1" stroke="currentColor" strokeWidth="2" />
              </svg>
            </button>
          </div>
        </div>
      </section>
    )
  }
  
  export default HeroSection