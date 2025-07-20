import requests
import telebot
import os

BOT_TOKEN = "8165194741:AAEHi3W8ZYZIzHHPBXUN1Kkk0r4zK-mtIDk"
OWNER_ID = 6896590701  # Your Telegram User ID

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == OWNER_ID:
        bot.send_message(OWNER_ID, "📡 Send me a direct download link (e.g. from SourceForge)")

@bot.message_handler(func=lambda m: m.chat.id == OWNER_ID)
def handle_link(message):
    url = message.text.strip()
    try:
        filename = url.split("/")[-1].split("?")[0]
        bot.send_message(OWNER_ID, f"📥 Downloading `{filename}`...", parse_mode="Markdown")

        r = requests.get(url, stream=True)
        size = int(r.headers.get('content-length', 0))
        if size > 2_000_000_000:
            bot.send_message(OWNER_ID, "❌ File is larger than 2GB. Telegram can't send it.")
            return

        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        with open(filename, 'rb') as f:
            bot.send_message(OWNER_ID, "✅ Uploading to Telegram...")
            bot.send_document(OWNER_ID, f)

        os.remove(filename)

    except Exception as e:
        bot.send_message(OWNER_ID, f"❌ Error: `{str(e)}`", parse_mode="Markdown")

bot.polling()