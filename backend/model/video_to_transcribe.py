import json
import yt_dlp
import whisper

def download_audio(youtube_url, output_template):
    """
    Downloads the audio from the provided YouTube URL using yt-dlp.
    
    Parameters:
        youtube_url (str): The URL of the YouTube video.
        output_template (str): Template for the output file, e.g., "audio.%(ext)s".
        
    Returns:
        str: The actual filename of the downloaded audio.
    """
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Use a valid audio codec.
            'preferredquality': '192',
        }],
        'quiet': False,
    }
    print("Downloading audio using yt-dlp...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    # The output template is like "audio.%(ext)s", so replace %(ext)s with 'mp3'
    final_filename = output_template.replace('%(ext)s', 'mp3')
    return final_filename

def group_transcript_by_minute(segments):
    """
    Groups Whisper transcription segments by 1-minute intervals.
    
    Parameters:
        segments (list): Each segment is a dict with keys 'start', 'end', and 'text'.
        
    Returns:
        dict: Keys are minute indexes (0, 1, 2, ...) and values are the concatenated texts.
    """
    transcript_by_minute = {}
    for segment in segments:
        start_time = segment["start"]
        text = segment["text"].strip()
        minute_index = int(start_time // 60)
        transcript_by_minute.setdefault(minute_index, []).append(text)
    
    # Concatenate segments for each minute
    for minute in transcript_by_minute:
        transcript_by_minute[minute] = " ".join(transcript_by_minute[minute])
    
    return transcript_by_minute

def main_video(youtube_url):
    # youtube_url = input("Enter YouTube URL: ").strip()
    # Set the output template with a placeholder for the extension.
    output_template = "audio.%(ext)s"
    
    # Download audio from YouTube and get the actual filename.
    audio_file = download_audio(youtube_url, output_template)
    print("Audio downloaded as", audio_file)
    
    # Load the Whisper model (choose model size as needed: tiny, base, small, medium, large)
    print("Loading Whisper model...")
    model = whisper.load_model("base")
    
    # Transcribe the audio file
    print("Transcribing audio...")
    result = model.transcribe(audio_file)
    segments = result.get("segments", [])
    
    # Group the transcription into minute-wise segments
    transcript_by_minute = group_transcript_by_minute(segments)
    
    # Save the result into a JSON file
    output_json = r"A:\Projects\Edu_Pro\backend\data\single.json"
    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(transcript_by_minute, f, ensure_ascii=False, indent=4)
    print("Transcript saved to", output_json)

