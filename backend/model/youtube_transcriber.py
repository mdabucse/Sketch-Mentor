import json
import os
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, TooManyRequests
import re

def extract_video_id(link):
    """
    Extracts the YouTube video ID from various URL formats.
    """
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", link)
    return match.group(1) if match else None

def get_transcript_one(video_link):
    try:
        # Extract video ID
        video_id = extract_video_id(video_link)
        
        if not video_id:
            raise ValueError("Invalid YouTube URL. Could not extract video ID.")

        print(f"Fetching transcript for video: {video_id}")
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = JSONFormatter()
        json_formatted = formatter.format_transcript(transcript)
        with open(r"A:\Projects\Edu_Pro\backend\data\single.json", "w", encoding="utf-8") as file:
            file.write(json_formatted)
        print(f"✅ Single transcript generated successfully for video: {video_id}")
        return json_formatted

    except ValueError as ve:
        print(f"❌ Error: {ve}")
        return None  # Return None instead of crashing
    
    except TranscriptsDisabled:
        print(f"❌ Error: Transcripts are disabled for video {video_id}.")
        return None
    
    except NoTranscriptFound:
        print(f"❌ Error: No transcript found for video {video_id}.")
        return None
    
    except TooManyRequests:
        print("❌ Error: Too many requests. Please wait and try again later.")
        return None
    
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return None

def get_transcript_all(video_ids):
    json_file_path = 'data/multi.json'
    
    try:
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r', encoding='utf-8') as file:
                transcripts = json.load(file)
                if not isinstance(transcripts, list):
                    transcripts = []
        else:
            transcripts = []
    except (FileNotFoundError, json.JSONDecodeError):
        transcripts = []
    
    formatter = JSONFormatter()
    
    for video_id in video_ids:
        try:
            print(f"Fetching transcript for video: {video_id}")
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            json_formatted = json.loads(formatter.format_transcript(transcript))
            transcripts.extend(json_formatted)

            print(f"✅ Transcript added for video: {video_id}")

        except TranscriptsDisabled:
            print(f"❌ Error: Transcripts are disabled for video {video_id}. Skipping...")
        except NoTranscriptFound:
            print(f"❌ Error: No transcript found for video {video_id}. Skipping...")
        except TooManyRequests:
            print("❌ Error: Too many requests. Please wait and try again later.")
            break
        except Exception as e:
            print(f"❌ Unexpected error for video {video_id}: {e}. Skipping...")

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(transcripts, json_file, ensure_ascii=False, indent=4)
    
    print("✅ Multi transcript JSON updated successfully!")
