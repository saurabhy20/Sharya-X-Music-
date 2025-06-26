# Shaurya X Music 🎧

A hacker-themed Telegram music bot that streams songs to group voice chats.

## Features

- `/play <song>` — Play music from YouTube in voice chat
- `/stop`, `/pause`, `/resume`, `/skip`
- `/help` — Command list
- `/ping` — Check if bot is alive
- Plugin system: Add features via `plugins/` directory
- Hacker-style branding (black, red, white)

## Setup and Run

1. **Clone & Install**

    ```bash
    git clone https://github.com/yourusername/shaurya-x-music.git
    cd shaurya-x-music
    pip install -r requirements.txt
    ```

2. **Configure Telegram API**

    - Get API credentials from [my.telegram.org](https://my.telegram.org)
    - Create a `.env` file in the root directory:

      ```
      API_ID=your_telegram_api_id
      API_HASH=your_telegram_api_hash
      BOT_TOKEN=your_telegram_bot_token
      OWNER_ID=your_telegram_user_id
      ```

3. **Install FFmpeg**

    - Linux: `sudo apt install ffmpeg`
    - Windows/Mac: [Download here](https://ffmpeg.org/download.html)

4. **Run the bot**

    ```bash
    python main.py
    ```

## Plugins

- Add Python files to `plugins/` for new features.
- Examples: `help.py`, `ping.py`, `music.py`
- Handlers are auto-loaded.

## Notes

- The bot must be admin in your group and able to join voice chats.
- For full hacker style, set a black/red/white profile picture and stickers.

---

> **Shaurya X Music** — Hack the beat! 🚩