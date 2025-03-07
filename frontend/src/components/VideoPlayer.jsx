import React from "react";
import ReactPlayer from "react-player";
import "../css/VideoPlayer.css";

const VideoPlayer = ({ videoUrl }) => {
  return (
    <div className="video-player">
      {videoUrl ? (
        <ReactPlayer url={videoUrl} width="100%" height="100%" controls />
      ) : (
        <p>No video selected.</p>
      )}
    </div>
  );
};

export default VideoPlayer;
