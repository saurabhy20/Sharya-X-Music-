from pyrogram import Client, filters

@Client.on_message(filters.command("help"))
async def help_command(client, message):
    text = (
        "🖤❤️🤍 <b>Shaurya X Music Help</b> 🤍❤️🖤\n\n"
        "<b>Commands:</b>\n"
        "<code>/play &lt;song&gt;</code> - Play a song in VC\n"
        "<code>/pause</code> - Pause playback\n"
        "<code>/resume</code> - Resume playback\n"
        "<code>/stop</code> - Stop music\n"
        "<code>/skip</code> - Skip current track\n"
        "<code>/ping</code> - Check if bot is alive\n"
        "<code>/help</code> - Show this message"
    )
    await message.reply(text, quote=True)
