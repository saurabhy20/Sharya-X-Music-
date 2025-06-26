# In utils/ffmpeg.py
import subprocess

def optimize_stream(url):
    cmd = f"ffmpeg -i {url} -ac 2 -f ogg -ar 48000 -b:a 128k pipe:1"
    process = subprocess.Popen(
        cmd.split(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    return process
