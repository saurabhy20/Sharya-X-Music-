@Client.on_message(filters.command("hack"))
async def hacker_mode(client, message):
    await message.reply_animation(
        animation="assets/hack.gif",
        caption=hacker_text("""
        🖥️ HACKER MODE ACTIVATED 🖥️
        
        • Encryption: AES-256
        • Bypass: Enabled
        • Security: ████████ 100%
        """)
    )
