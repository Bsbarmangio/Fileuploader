import requests
import telebot
import os
from telebot import apihelper

apihelper.READ_TIMEOUT = 60
apihelper.CONNECTION_TIMEOUT = 30

BOT_TOKEN = "8165194741:AAEHi3W8ZYZIzHHPBXUN1Kkk0r4zK-mtIDk"
OWNER_ID = 6896590701  # Your Telegram User ID

bot = telebot.TeleBot(BOT_TOKEN, timeout=60)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == OWNER_ID:
        bot.send_message(OWNER_ID, "📡 Send me a direct download link (e.g. SourceForge, GitHub, etc.)")

@bot.message_handler(func=lambda m: m.chat.id == OWNER_ID)
def handle_link(message):
    url = message.text.strip()
    try:
        filename = url.split("/")[-1].split("?")[0]
        status_msg = bot.send_message(OWNER_ID, f"📥 Downloading `{filename}`... please wait", parse_mode="Markdown")

        r = requests.get(url, stream=True)
        total = int(r.headers.get('content-length', 0))
        if total > 2_000_000_000:
            bot.send_message(OWNER_ID, "❌ File is larger than 2GB. Telegram can't send it.")
            return

        downloaded = 0
        last_percent = 0
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 128):  # 128 KB chunks
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if total > 0:
                        percent = int((downloaded / total) * 100)
                        if percent - last_percent >= 10:
                            last_percent = percent
                            bot.send_message(OWNER_ID, f"📊 Downloaded {percent}%")

        with open(filename, 'rb') as f:
            bot.send_message(OWNER_ID, "✅ Uploading to Telegram...")
            bot.send_document(OWNER_ID, f)

        os.remove(filename)

    except Exception as e:
        bot.send_message(OWNER_ID, f"❌ Error: `{str(e)}`", parse_mode="Markdown")

bot.polling()
