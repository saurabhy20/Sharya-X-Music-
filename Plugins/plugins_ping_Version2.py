from pyrogram import Client, filters

@Client.on_message(filters.command("ping"))
async def ping_command(client, message):
    await message.reply("🖤❤️🤍 <b>Pong!</b> 🤍❤️🖤", quote=True)