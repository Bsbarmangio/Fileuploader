import requests
import telebot
import os
from telebot import apihelper  # ✅ Timeout fix

# Set Telegram API timeouts (compatible with older pyTelegramBotAPI versions)
apihelper.READ_TIMEOUT = 60
apihelper.CONNECTION_TIMEOUT = 30

BOT_TOKEN = "7835124466:AAGhfA1yKweBuHb8ukov550OeqRTtfNRh8c"

OWNER_ID = 6896590701

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id == OWNER_ID:
        bot.send_message(OWNER_ID, "📡 Send me a direct download link")

@bot.message_handler(func=lambda m: m.chat.id == OWNER_ID)
def handle_link(message):
    url = message.text.strip()
    try:
        filename = url.split("/")[-1].split("?")[0]
        status_msg = bot.send_message(OWNER_ID, f"📥 Downloading `{filename}`...", parse_mode="Markdown")

        r = requests.get(url, stream=True)
        total = int(r.headers.get('content-length', 0))
        if total > 2_000_000_000:
            bot.send_message(OWNER_ID, "❌ File is larger than 2GB. Telegram can't send it.")
            return

        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 128):
                if chunk:
                    f.write(chunk)

        bot.send_message(OWNER_ID, "📤 Uploading to Telegram...")
        with open(filename, 'rb') as f:
            bot.send_document(OWNER_ID, f)

        os.remove(filename)

    except Exception as e:
        bot.send_message(OWNER_ID, f"❌ Error: `{str(e)}`", parse_mode="Markdown")

bot.polling()