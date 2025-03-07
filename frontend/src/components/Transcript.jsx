import React, { useEffect, useState } from "react";
import "../css/transcript.css";

const Transcript = () => {
  const [transcript, setTranscript] = useState([]);

  useEffect(() => {
    const fetchTranscript = async () => {
      try {
        const response = await fetch("https://w4gw8kvg-5000.inc1.devtunnels.ms/load_transcribe");
        if (!response.ok) {
          throw new Error("Failed to fetch transcript");
        }
        const data = await response.json();
        formatTranscript(data);
      } catch (error) {
        setTranscript(["Error loading transcript"]);
        console.error("Error fetching transcript:", error);
      }
    };

    fetchTranscript();
  }, []);

  // Function to format the transcript content
  const formatTranscript = (data) => {
    if (data.message) {
      const text = Object.values(data.message).join(" ");
      const points = text.split(". ").filter(line => line.trim() !== ""); // Splitting into points
      setTranscript(points.map((point, index) => (
        <p key={index} className="transcript-line">
          {index + 1}. {point}.
        </p>
      )));
    } else {
      setTranscript(["Invalid transcript format"]);
    }
  };

  return (
    <div className="transcript">
      <h2 className="transcript-title">Transcript</h2>
      <div className="transcript-content">
        {transcript.length > 0 ? transcript : <p>Loading...</p>}
      </div>
    </div>
  );
};

export default Transcript;