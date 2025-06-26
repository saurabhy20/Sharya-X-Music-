from yt_dlp import YoutubeDL
import os

queues = {}
current_stream = {}

def yt_search(query):
    opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': True
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        return info['entries'][0]['url'], info['entries'][0]['title']

async def download_and_stream(url, chat_id):
    out = f"downloads/{chat_id}_song.mp3"
    opts = {
        'format': 'bestaudio',
        'outtmpl': out,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    with YoutubeDL(opts) as ydl:
        ydl.download([url])
    return out
