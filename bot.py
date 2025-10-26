import os
import re
from pyrogram import Client, filters
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler

# Telegram bot credentials
api_id = int(os.environ.get("API_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("BOT_TOKEN")

app = Client("link_remover_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

url_pattern = re.compile(r"(https?://\S+|www\.\S+)")

@app.on_message(filters.group & filters.text)
async def delete_links(client, message):
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    if chat_member.status in ["administrator", "creator"]:
        return
    if url_pattern.search(message.text):
        try:
            await message.delete()
        except:
            pass

# Dummy HTTP server to satisfy Koyeb Web Service health check
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

def run_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), Handler)
    server.serve_forever()

# Start HTTP server in a separate thread
Thread(target=run_server).start()

print("Bot is running...")
app.run()
