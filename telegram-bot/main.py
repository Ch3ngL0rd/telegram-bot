
import os
import openai
import logging
import asyncio

from dotenv import load_dotenv
from telegram import ReactionTypeEmoji, Update, constants
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    CommandHandler,
    ContextTypes,
)

import workout
import uuid
from proto_stubs import telegram_message_pb2

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Received /start command from user %s", update.effective_user.id)
    await update.message.reply_text(
        "Hello! I'm ZacTelegramBot. Voice, images and text are accepted."
    )


async def react(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id
    msg_id = update.message.message_id
    reaction = ReactionTypeEmoji(constants.ReactionEmoji.THUMBS_UP)
    await context.bot.set_message_reaction(
        chat_id=chat_id, message_id=msg_id, reaction=[reaction], is_big=False
    )


async def ingest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    openai_key = os.getenv("OPENAI_KEY")
    wh = workout.WorkoutHandler(openai_key)
    user = update.effective_user.id if update.effective_user else "unknown"
    if not update.message.text:
        logger.info("Received non-text message from user %s", user)
        return

    logger.info("Received message from user %s: %r", user, update.message.text)

    message = telegram_message_pb2.TelegramMessageV1(
        event_id=generateEventID(),
        chat_id=update.message.chat_id,
        user_id=update.effective_user.id,
        kind=telegram_message_pb2.MediaKind.TEXT,
        text=update.message.text,
    )

    response = wh.handleTelegramMessage(message)

    asyncio.create_task(react(update, context))
    await update.message.reply_text(response)
    


def generateEventID() -> str:
    return str(uuid.uuid4())


def main():
    load_dotenv()
    telegram_token = os.getenv("TELEGRAM_TOKEN")
    if not telegram_token:
        logger.error("TELEGRAM_TOKEN is not set in the .env file")
        raise ValueError("TELEGRAM_TOKEN is not set in the .env file")
    openai_key = os.getenv("OPENAI_KEY")
    if not openai_key:
        logger.error("OPENAI_KEY is not set in the .env file")
        raise ValueError("OPENAI_KEY is not set in the .env file")
    logger.info("Starting ZacTelegramBot...")

    application = Application.builder().token(telegram_token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(
        MessageHandler(filters.TEXT | filters.PHOTO | filters.VOICE, ingest)
    )
    application.run_polling()


if __name__ == "__main__":
    main()
