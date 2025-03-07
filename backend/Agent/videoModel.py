from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import os
import subprocess
import shutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("video-api")

app = FastAPI()

# Mount the media directory for serving video files
media_directory = "media"
os.makedirs(os.path.join(media_directory, "videos"), exist_ok=True)
app.mount("/media", StaticFiles(directory=media_directory), name="media")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VisualizationRequest(BaseModel):
    problem: str

@app.post("/videoGeneration")
async def generate_video(req: VisualizationRequest, request: Request):
    logger.info(f"Received video generation request for problem: {req.problem}")
    
    try:
        from AI_MATH_AGENT.VideoModel.pipeline import AgenticPipeline
        from AI_MATH_AGENT.VideoModel.prompts import PROMPTS
        
        pipeline = AgenticPipeline()
        user_prompt = req.problem
        
        pipeline_result = pipeline.run(user_prompt)
        
        if pipeline_result["status"] not in ["success", "fallback"]:
            logger.error(f"Pipeline failed with status: {pipeline_result['status']}")
            raise Exception("Pipeline failed to generate code.")
        
        # Ensure a unique filename to avoid conflicts
        import uuid
        unique_id = uuid.uuid4().hex[:8]
        file_name = f"manim_visualization_{unique_id}.py"
        file_path = os.path.join(os.getcwd(), file_name)
        
        logger.info(f"Writing generated code to {file_path}")
        with open(file_path, "w") as f:
            f.write(pipeline_result["code"])
        
        scene_name = "VisualizationVideo"
        
        # Run manim with proper quality settings
        manim_command = ["manim", "-pql", file_path, scene_name]
        logger.info(f"Running Manim command: {' '.join(manim_command)}")
        
        proc_result = subprocess.run(manim_command, capture_output=True, text=True)
        if proc_result.returncode != 0:
            logger.error(f"Manim command failed with error: {proc_result.stderr}")
            raise Exception(f"Manim error: {proc_result.stderr}")
        
        # Determine the actual output path from manim
        base_name = os.path.splitext(os.path.basename(file_path))[0]
        quality = "480p15"  # This should match your manim settings
        output_dir = os.path.join("media", "videos", base_name, quality)
        output_file = os.path.join(output_dir, f"{scene_name}.mp4")
        
        # Check if the output file exists
        if not os.path.exists(output_file):
            logger.error(f"Output video file not found at: {output_file}")
            # Try to find the actual video file
            expected_dir = os.path.join(os.getcwd(), "media", "videos", base_name)
            if os.path.exists(expected_dir):
                for root, dirs, files in os.walk(expected_dir):
                    for file in files:
                        if file.endswith(".mp4"):
                            found_file = os.path.join(root, file)
                            logger.info(f"Found video at: {found_file}")
                            relative_path = os.path.relpath(found_file, os.path.join(os.getcwd(), "media"))
                            output_file = os.path.join("media", relative_path)
            else:
                logger.error(f"Expected directory not found: {expected_dir}")
                raise Exception("Video generation failed - output file not found")
        
        # Construct the proper video URL based on the host
        host = request.headers.get("host", "localhost:8001")
        scheme = request.headers.get("x-forwarded-proto", "http")
        base_url = f"{scheme}://{host}"
        
        # Construct the video URL with the proper base URL
        video_path = f"{base_url}/{output_file}"
        logger.info(f"Video generated successfully at: {video_path}")
        
        # Clean up the temporary python file
        try:
            os.remove(file_path)
        except Exception as e:
            logger.warning(f"Could not remove temporary file {file_path}: {str(e)}")
        
        return {"video_path": video_path, "status": "success"}
        
    except Exception as e:
        logger.exception(f"Error in video generation: {str(e)}")
        # Build fallback video URL using a relative path
        host = request.headers.get("host", "localhost:8001")
        scheme = request.headers.get("x-forwarded-proto", "http")
        base_url = f"{scheme}://{host}"
        # Use a relative path inside the media directory and fix the extension to .mp4
        fallback_video = "videos/manim_visualization_181bc014/480p15/ReliableQuadraticVisualization.mp4"
        fallback_video_path = f"{base_url}/media/{fallback_video}"
        logger.info(f"Returning fallback video at: {fallback_video_path}")
        return {"video_path": fallback_video_path, "status": "fallback"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)