import React, { useEffect, useRef, useState } from "react";
import { FaPencil } from "react-icons/fa6";
import { FaEraser } from "react-icons/fa6";
import { RiRectangleFill } from "react-icons/ri";
import { FaCircle } from "react-icons/fa6";
import { TbLine } from "react-icons/tb";
import { VscRunAll } from "react-icons/vsc";
import { MdOutlineRefresh } from "react-icons/md";
import axios from "axios";
import "../css/canvasStyles.css";

const Canvas = () => {
const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [color, setColor] = useState("#ffffff");
  const [lineWidth, setLineWidth] = useState(3);
  const [shape, setShape] = useState("free");
  const [startPos, setStartPos] = useState(null);
  const [isErasing, setIsErasing] = useState(false);
  const [activeTool, setActiveTool] = useState("free");
  const [responseText, setResponseText] = useState("");

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    ctx.lineCap = "round";
    ctx.lineJoin = "round";
  }, []);

  const startDrawing = (e) => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    if (isErasing) {
      const size = lineWidth * 2;
      ctx.clearRect(e.nativeEvent.offsetX - size / 2, e.nativeEvent.offsetY - size / 2, size, size);
    } else if (shape === "free") {
      ctx.strokeStyle = color;
      ctx.lineWidth = lineWidth;
      ctx.beginPath();
      ctx.moveTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
    } else {
      setStartPos({ x: e.nativeEvent.offsetX, y: e.nativeEvent.offsetY });
    }
    setIsDrawing(true);
  };

  const draw = (e) => {
    if (!isDrawing) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    if (isErasing) {
      ctx.clearRect(e.nativeEvent.offsetX, e.nativeEvent.offsetY, lineWidth, lineWidth);
    } else if (shape === "free") {
      ctx.lineTo(e.nativeEvent.offsetX, e.nativeEvent.offsetY);
      ctx.stroke();
    }
  };

  const stopDrawing = (e) => {
    if (!isDrawing) return;
    setIsDrawing(false);

    if (isErasing) return;

    if (shape !== "free" && startPos) {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext("2d");
      ctx.strokeStyle = color;
      ctx.lineWidth = lineWidth;
      const endX = e.nativeEvent.offsetX;
      const endY = e.nativeEvent.offsetY;

      if (shape === "rectangle") {
        ctx.strokeRect(startPos.x, startPos.y, endX - startPos.x, endY - startPos.y);
      } else if (shape === "circle") {
        const radius = Math.sqrt((endX - startPos.x) ** 2 + (endY - startPos.y) ** 2);
        ctx.beginPath();
        ctx.arc(startPos.x, startPos.y, radius, 0, 2 * Math.PI);
        ctx.stroke();
      } else if (shape === "line") {
        ctx.beginPath();
        ctx.moveTo(startPos.x, startPos.y);
        ctx.lineTo(endX, endY);
        ctx.stroke();
      }
    }
  };

  const resetCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
  };

  const selectTool = (tool) => {
    setActiveTool(tool);
    setIsErasing(tool === "eraser");
    if (tool !== "eraser") setShape(tool);
  };

  //**Updated runBackendAnalysis Function**
  const runBackendAnalysis = async () => {
    const canvas = canvasRef.current;
    if (!canvas) {
      console.error("Canvas reference not found.");
      setResponseText("Error: Canvas not found.");
      return;
    }
  
    const ctx = canvas.getContext("2d");
  
    // to check if canvas has any content 
    const hasContent = (() => {
      const pixelData = ctx.getImageData(0, 0, canvas.width, canvas.height).data;
      for (let i = 0; i < pixelData.length; i += 4) {
        if (pixelData[i + 3] !== 0) {
          // Alpha (opacity) channel is not 0, meaning there's something drawn.
          return true;
        }
      }
      return false;
    })();
  
    if (!hasContent) {
      console.error("Canvas is empty. Please draw something.");
      setResponseText("Error: Please draw something before running.");
      return;
    }
  
    // Convert canvas to base64 image
    const imageData = canvas.toDataURL("image/png");
  
    if (!imageData || imageData.length < 100) {
      console.error("Image data is empty or too small.");
      setResponseText("Error: Image data is invalid.");
      return;
    }
  
    try {
      console.log("Sending image data to backend...");
  
      const response = await axios.post(
        "https://w4gw8kvg-8900.inc1.devtunnels.ms/calculate",
        { image: imageData, dict_of_vars: {} },
        { headers: { "Content-Type": "application/json" } }
      );
  
      console.log("Backend Response:", response.data);
  
      if (
        response.data &&
        Array.isArray(response.data.data) &&
        response.data.data.length > 0
      ) {
        const resultObj = response.data.data[0]; // Extract first item
      
        setResponseText(`${resultObj.expr} = ${resultObj.result}`);
      
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "black";
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "white";
        ctx.font = "bold 24px gorilla";
      
        console.log("Drawing on Canvas:", resultObj.expr, resultObj.result); // Debugging
      
        ctx.fillText(`Expression: ${resultObj.expr}`, 20, 50);
        ctx.fillText(`Result: ${resultObj.result}`, 20, 100);
      } else {
        console.error("Unexpected backend response format:", response.data);
        setResponseText("Error: Unexpected backend response.");
      }      
    }
       catch (error) {
      console.error("Error calling backend:", error);
      setResponseText("Network error. Check backend server.");
    }
  };

  return (
    <div>
    {/* <div className="tool-bar">Tool Bar</div> */}
              <div className="toolbar">
            <button 
              className={activeTool === "free" ? "active" : ""} 
              onClick={() => selectTool("free")} 
            >
              <FaPencil />
              <span className="tooltip">Pen</span>
            </button>

            <button 
              className={activeTool === "rectangle" ? "active" : ""} 
              onClick={() => selectTool("rectangle")} 
            >
              <RiRectangleFill />
              <span className="tooltip">Rectangle</span>
            </button>

            <button 
              className={activeTool === "circle" ? "active" : ""} 
              onClick={() => selectTool("circle")} 
            >
              <FaCircle />
              <span className="tooltip">Circle</span>
            </button>

            <button 
              className={activeTool === "line" ? "active" : ""} 
              onClick={() => selectTool("line")} 
            >
              <TbLine />
              <span className="tooltip">Line</span>
            </button>

            <button 
              className={activeTool === "eraser" ? "active" : ""} 
              onClick={() => selectTool("eraser")} 
            >
              <FaEraser />
              <span className="tooltip">Eraser</span>
            </button>

            <input 
              type="range" 
              min="5" 
              max="50" 
              value={lineWidth} 
              onChange={(e) => setLineWidth(e.target.value)} 
              title="Line Width"
            />

            <input 
              type="color" 
              value={color} 
              onChange={(e) => setColor(e.target.value)} 
              disabled={isErasing} 
              title="Color"
            />

            <button 
              onClick={runBackendAnalysis} 
            >
              <VscRunAll />
              <span className="tooltip">Run</span>
            </button>

            <button 
              onClick={resetCanvas} 
            >
              <MdOutlineRefresh />
              <span className="tooltip">Reset</span>
            </button>
          </div>

    {/* <div className="canvas">Canvas</div> */}
    <div className="canvas">
            <canvas
              ref={canvasRef}
              className="drawing-canvas"
              onMouseDown={startDrawing}
              onMouseMove={draw}
              onMouseUp={stopDrawing}
              onMouseOut={stopDrawing}
            />
          </div>
    </div>
  )
};

export default Canvas;