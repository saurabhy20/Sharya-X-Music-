import os
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import InputStream, AudioPiped
from yt_dlp import YoutubeDL

from config import OWNER_ID

# The call_py instance will be imported from main.py during runtime
call_py: PyTgCalls = None

# Song queue per chat (optional, can be expanded)
queues = {}

def yt_search(query):
    opts = {'format': 'bestaudio', 'noplaylist':True, 'quiet':True}
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]
    return info['url'], info['title']

async def download_and_stream(url, chat_id):
    out = f"{chat_id}_song.mp3"
    opts = {
        'format': 'bestaudio',
        'noplaylist':True,
        'quiet':True,
        'outtmpl': out,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }
    with YoutubeDL(opts) as ydl:
        ydl.download([url])
    return out

@Client.on_message(filters.command("start"))
async def start(_, m):
    await m.reply("🖤 Welcome to <b>Shaurya X Music</b>!\nType <code>/play &lt;song&gt;</code> to get started.", quote=True)

@Client.on_message(filters.command("play") & filters.group)
async def play(client, m):
    global call_py
    if call_py is None:
        from main import call_py as main_call_py
        call_py = main_call_py

    user = m.from_user.mention if m.from_user else "someone"
    if len(m.command) < 2:
        return await m.reply("Usage: <code>/play &lt;song name or YouTube link&gt;</code>")
    query = " ".join(m.command[1:])
    await m.reply(f"🖤 Searching for: <b>{query}</b> ...")
    if "youtube.com" in query or "youtu.be" in query:
        url = query
        title = "YouTube Link"
    else:
        url, title = yt_search(query)
    await m.reply(f"❤️ Downloading: <b>{title}</b>")
    audio_file = await download_and_stream(url, m.chat.id)
    await call_py.join_group_call(
        m.chat.id,
        InputStream(
            AudioPiped(audio_file)
        ),
        stream_type="local"
    )
    await m.reply(f"🤍 Now playing: <b>{title}</b> in VC!\nRequested by {user}")

@Client.on_message(filters.command("stop") & filters.group)
async def stop(client, m):
    global call_py
    if call_py is None:
        from main import call_py as main_call_py
        call_py = main_call_py
    await call_py.leave_group_call(m.chat.id)
    await m.reply("❤️ Music stopped!")

@Client.on_message(filters.command("pause") & filters.group)
async def pause(client, m):
    global call_py
    if call_py is None:
        from main import call_py as main_call_py
        call_py = main_call_py
    await call_py.pause_stream(m.chat.id)
    await m.reply("🖤 Paused!")

@Client.on_message(filters.command("resume") & filters.group)
async def resume(client, m):
    global call_py
    if call_py is None:
        from main import call_py as main_call_py
        call_py = main_call_py
    await call_py.resume_stream(m.chat.id)
    await m.reply("🤍 Resumed!")

@Client.on_message(filters.command("skip") & filters.group)
async def skip(client, m):
    global call_py
    if call_py is None:
        from main import call_py as main_call_py
        call_py = main_call_py
    await call_py.leave_group_call(m.chat.id)
    await m.reply("❤️ Skipped current song!")
