import re
import yt_dlp
import ffmpeg
import os
import uuid

from django.conf import settings

def  download_youtube_audio(video_url, category):
    yt_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'downloaded_audio.%(ext)s',
    }

    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        downloaded_ext = info.get("ext", "unknown") #Detect actual format of video file
        title = info.get('title', 'Unknown Title')

        #Create input with detected format
        input_file = f"downloaded_audio.{downloaded_ext}"

        #Generate a safe filename
        safe_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')[:20] #Limit to 20 chars
        
        #Ensure uniquenss using a UUID
        unique_id = str(uuid.uuid4())[:8] #Generate a short random string
        output_folder = os.path.join(settings.MEDIA_ROOT, 'audios', category)
        os.makedirs(output_folder, exist_ok=True) #Create folder if it doesn't exist

        output_file = os.path.join(output_folder,f"{safe_title}_{unique_id}.mp3")

        ffmpeg.input(input_file).output(output_file, format='mp3').run(cmd="ffmpeg")
        
        #Clean up files
        os.remove(input_file)

        return title, os.path.relpath(output_file, settings.MEDIA_ROOT)
