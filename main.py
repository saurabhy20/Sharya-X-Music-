import asyncio
import os
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped, AudioVideoPiped
from yt_dlp import YoutubeDL
from config import API_ID, API_HASH, BOT_TOKEN, OWNER_ID
import subprocess
from typing import Tuple, Dict, List

# ==================== CONSTANTS ====================
RED = "\033[1;31m"
WHITE = "\033[1;37m"
BLACK = "\033[1;30m"
RESET = "\033[0m"

# ==================== BANNER ====================
print(f"""{RED}
███████╗██╗  ██╗ █████╗ ██╗   ██╗██████╗ ██╗   ██╗ █████╗
██╔════╝██║  ██║██╔══██╗██║   ██║██╔══██╗╚██╗ ██╔╝██╔══██╗
███████╗███████║███████║██║   ██║██║██║   ╚████╔╝ ███████║
╚════██║██╔══██║██╔══██║██║   ██║██║  ██║  ╚██╔╝  ██╔══ ██║
███████║██║  ██║██║  ██║╚██████╔╝██    ██╔╝ ██║   ██║    ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝    ╚═╝
{WHITE}        Shaurya X Music - Hacker Edition 🚩
{RESET}""")

# ==================== INITIALIZATION ====================
app = Client(
    "shaurya_x_music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

# ==================== GLOBAL VARIABLES ====================
queues: Dict[int, List[Dict[str, str]]] = {}
current_stream: Dict[int, Dict[str, str]] = {}

# ==================== HELPER FUNCTIONS ====================
def hacker_text(text: str) -> str:
    return f"{RED}⚡{WHITE} {text} {RED}⚡{RESET}"

async def yt_search(query: str) -> Tuple[str, str]:
    opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
        'extract_flat': True
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=False)
        if not info or not info.get('entries'):
            return None, None
        return info['entries'][0]['url'], info['entries'][0]['title']

async def download_audio(url: str, chat_id: int) -> str:
    out_file = f"downloads/{chat_id}_song.mp3"
    opts = {
        'format': 'bestaudio',
        'outtmpl': out_file,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True
    }
    
    try:
        with YoutubeDL(opts) as ydl:
            ydl.download([url])
        return out_file
    except Exception as e:
        print(f"{RED}Download error: {e}{RESET}")
        return None

# ==================== BOT COMMANDS ====================
@app.on_message(filters.command("start"))
async def start(_, m: Message):
    await m.reply(
        hacker_text("Welcome to Shaurya X Music Bot!"),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📜 Commands", callback_data="help")],
            [InlineKeyboardButton("🔊 Join Channel", url="https://t.me/YourChannel")]
        ])
    )

@app.on_message(filters.command("play") & filters.group)
async def play(_, m: Message):
    if len(m.command) < 2:
        return await m.reply(hacker_text("Usage: /play <song name or YouTube link>"))
    
    query = " ".join(m.command[1:])
    await m.reply(hacker_text(f"Searching for: {query}"))
    
    if "youtube.com" in query or "youtu.be" in query:
        url = query
        title = "YouTube Link"
    else:
        url, title = await yt_search(query)
        if not url:
            return await m.reply(hacker_text("Song not found!"))
    
    await m.reply(hacker_text(f"Downloading: {title}"))
    audio_file = await download_audio(url, m.chat.id)
    
    if not audio_file:
        return await m.reply(hacker_text("Download failed!"))
    
    try:
        await call_py.join_group_call(
            m.chat.id,
            AudioPiped(audio_file),
            stream_type="local"
        )
        current_stream[m.chat.id] = {
            'file': audio_file,
            'title': title,
            'requester': m.from_user.mention
        }
        await m.reply(
            hacker_text(f"Now playing: {title}"),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⏸ Pause", callback_data="pause"),
                 InlineKeyboardButton("⏭ Skip", callback_data="skip")]
            ])
        )
    except Exception as e:
        await m.reply(hacker_text(f"Error: {str(e)}"))
        if os.path.exists(audio_file):
            os.remove(audio_file)

# ==================== CONTROL COMMANDS ====================
@app.on_message(filters.command("pause") & filters.group)
async def pause(_, m: Message):
    try:
        await call_py.pause_stream(m.chat.id)
        await m.reply(hacker_text("Playback paused"))
    except Exception as e:
        await m.reply(hacker_text(f"Error: {str(e)}"))

@app.on_message(filters.command("resume") & filters.group)
async def resume(_, m: Message):
    try:
        await call_py.resume_stream(m.chat.id)
        await m.reply(hacker_text("Playback resumed"))
    except Exception as e:
        await m.reply(hacker_text(f"Error: {str(e)}"))

@app.on_message(filters.command("skip") & filters.group)
async def skip(_, m: Message):
    try:
        await call_py.leave_group_call(m.chat.id)
        if m.chat.id in current_stream:
            if os.path.exists(current_stream[m.chat.id]['file']):
                os.remove(current_stream[m.chat.id]['file'])
            del current_stream[m.chat.id]
        await m.reply(hacker_text("Skipped current track"))
    except Exception as e:
        await m.reply(hacker_text(f"Error: {str(e)}"))

# ==================== EVENT HANDLERS ====================
@call_py.on_stream_end()
async def stream_end_handler(_, update):
    chat_id = update.chat_id
    if chat_id in current_stream:
        if os.path.exists(current_stream[chat_id]['file']):
            os.remove(current_stream[chat_id]['file'])
        del current_stream[chat_id]
    print(f"{RED}Stream ended in chat {chat_id}{RESET}")

# ==================== MAIN FUNCTION ====================
async def main():
    # Create downloads directory if not exists
    if not os.path.exists("downloads"):
        os.makedirs("downloads")
    
    await app.start()
    print(f"{WHITE}Bot started{RESET}")
    await call_py.start()
    print(f"{WHITE}PytgCalls started{RESET}")
    await idle()
    await app.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"{RED}Bot stopped by user{RESET}")
    except Exception as e:
        print(f"{RED}Fatal error: {e}{RESET}")
