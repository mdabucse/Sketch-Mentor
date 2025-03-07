import youtube_dl
import speech_recognition as sr
import os

def download_audio(url, output_file):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': output_file,
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    
    try:
        text = recognizer.recognize_google(audio)
        return text
    except sr.UnknownValueError:
        print("Speech recognition could not understand the audio")
    except sr.RequestError as e:
        print(f"Could not request results from the speech recognition service; {e}")

def youtube_to_text(video_url):
    audio_file = "temp_audio.wav"
    
    # Download audio from YouTube video
    download_audio(video_url, audio_file)
    
    # Transcribe the audio
    transcript = transcribe_audio(audio_file)
    
    # Clean up temporary audio file
    os.remove(audio_file)
    
    return transcript

# Example usage
video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with your YouTube video URL
text = youtube_to_text(video_url)
print(text)
