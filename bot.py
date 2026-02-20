import requests
from telegram.ext import Updater, MessageHandler, Filters
from telegram import ParseMode

TELEGRAM_TOKEN = "7575731084:AAF81FrFiT3wX5NtpMY2IumKhZ2Djq_7ajk"
GEMINI_API_KEY = "AIzaSyBkchTlvhiAvvQObr16rbTrT3M0741zIzI"
BOT_USERNAME = "YourBotUsername"  # نام رباتت بدون @

def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}"
    body = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        r = requests.post(url, json=body)
        data = r.json()
        return data["candidates"][0]["content"]["parts"][0]["text"]
    except:
        return "خطا در اتصال به جمینای"

def reply_handler(update, context):
    message = update.message
    text = message.text

    should_answer = False
    question = ""

    if message.reply_to_message and message.reply_to_message.from_user.username == BOT_USERNAME:
        should_answer = True
        question = text

    if f"@{BOT_USERNAME}" in text:
        should_answer = True
        question = text.replace(f"@{BOT_USERNAME}", "").strip()

    if not should_answer:
        return

    answer = ask_gemini(question)
    message.reply_text(answer, parse_mode=ParseMode.MARKDOWN)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
