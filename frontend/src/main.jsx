// import React from 'react'
// import ReactDOM from 'react-dom/client'
// import App from './App.jsx'
// import './styles.css'

// ReactDOM.createRoot(document.getElementById('root')).render(
//   <React.StrictMode>
//     <App />
//   </React.StrictMode>,
// )

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './styles.css'
import { BrowserRouter, Routes, Route } from 'react-router-dom'; // Import BrowserRouter, Routes, and Route
import SketchMentorUI from "../src/components/SketchMentorUI.jsx"; // Import your SketchMentorUI component
import HeroSection from '../src/components/HeroSection.jsx';
import Home from './components/Home.jsx';
import Solve from './components/solve.jsx';
import MathVisualization from './components/MathVisualization.jsx';
import Visual from './components/Visual.jsx';
import Transcript from './components/Transcript.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} /> {/*  Keep your existing App component route */}
        <Route path="/sketch-mentor" element={<SketchMentorUI />} /> {/* Route for SketchMentorUI */}
        <Route path="/hero" element={<HeroSection />} />
        <Route path="/home" element={<Home />} />
        <Route path='/solve' element={<Solve />} />
        <Route path='/math-visualization' element={<MathVisualization />} />
        <Route path='/visual' element={<Visual />} />
        <Route path='/transcript' element={<Transcript />} />
      </Routes>
    </BrowserRouter>
  </React.StrictMode>,
)
