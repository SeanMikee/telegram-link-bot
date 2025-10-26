import os
import re
from pyrogram import Client, filters

# Load credentials from environment variables
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

app = Client("link_remover_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# Regex to detect links
url_pattern = re.compile(r"(https?://\S+|www\.\S+)")

@app.on_message(filters.group & filters.text)
async def delete_links(client, message):
    # Skip admins
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status in ["administrator", "creator"]:
        return

    # Delete message if it contains a link
    if url_pattern.search(message.text):
        try:
            await message.delete()
        except:
            pass

print("Bot is running...")
app.run()
