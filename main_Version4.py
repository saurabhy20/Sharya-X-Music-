import asyncio
import os
import glob
import importlib
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from config import API_ID, API_HASH, BOT_TOKEN

# Colors for hacker theme (console output)
RED = "\033[1;31m"
WHITE = "\033[1;37m"
BLACK = "\033[1;30m"
RESET = "\033[0m"

# ASCII banner
print(f"""{RED}
███████╗██╗  ██╗ █████╗ ██╗   ██╗██████╗ ██╗   ██╗ █████╗
██╔════╝██║  ██║██╔══██╗██║   ██║██╔══██╗╚██╗ ██╔╝██╔══██╗
███████╗███████║███████║██║   ██║██║  ██║ ╚████╔╝ ███████║
╚════██║██╔══██║██╔══██║██║   ██║██║  ██║  ╚██╔╝  ██╔══██║
███████║██║  ██║██║  ██║╚██████╔╝██████╔╝   ██║   ██║  ██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝
{WHITE}        Shaurya X Music - Hacker Edition 🚩
{RESET}""")

app = Client("shaurya_x_music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

def load_plugins():
    plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
    plugin_files = glob.glob(os.path.join(plugins_dir, "*.py"))
    for plugin_path in plugin_files:
        plugin_name = os.path.basename(plugin_path)[:-3]
        if plugin_name == "__init__":
            continue
        importlib.import_module(f"plugins.{plugin_name}")

async def main():
    load_plugins()
    await app.start()
    await call_py.start()
    print(f"{WHITE}Shaurya X Music with plugin support is online!{RESET}")
    await idle()
    await app.stop()

if __name__ == "__main__":
    asyncio.run(main())