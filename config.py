import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", 12345))
    API_HASH = os.getenv("API_HASH", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    OWNER_ID = int(os.getenv("OWNER_ID", 0))
    SESSION = os.getenv("SESSION_STRING", "")
    CHAT_ID = int(os.getenv("MUSIC_CHAT_ID", -10012345))
