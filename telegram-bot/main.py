import os
from generated.telegram_message_pb2 import RawMessageV1, FilePointer, MediaKind

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application, MessageHandler, filters, CommandHandler, ContextTypes
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Hello! I'm ZacTelegramBot. Voice, images and text are accepted.")

async def ingest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    m = update.message
    if m.text:
        await m.reply_text(f"Received text: {m.text}")
    elif m.photo:
        await m.reply_text("Received a photo!")
    elif m.voice:
        await m.reply_text("Received a voice message!")
    else:
        await m.reply_text("Received an unsupported message type.")
    await m.reply_text("Ingested the message successfully!")

def main():
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        raise ValueError("TELEGRAM_TOKEN is not set in the .env file")
    application = Application.builder().token(telegram_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VOICE, ingest))
    application.run_polling()

if __name__ == "__main__":
    main()