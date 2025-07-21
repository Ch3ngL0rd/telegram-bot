import os
import openai
import logging

from dotenv import load_dotenv
from telegram import ReactionTypeEmoji, Update, constants
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    CommandHandler,
    ContextTypes,
)
from typing import Union, Literal, Optional
from pydantic import BaseModel, Field

# Different ways to measure exercise:
# reps (kg optional, )
# time based - seconds, minutes + (distance


class ExerciseBase(BaseModel):
    exerciseName: str
    weightInKilograms: Optional[float] = None
    distanceInMeters: Optional[float] = None


class RepsExercise(ExerciseBase):
    type: Literal["reps"] = Field("reps", Literal=True)
    reps: int
    repsInReserve: Optional[int] = None


class DurationExercise(ExerciseBase):
    type: Literal["duration"] = Field("duration", Literal=True)
    durationInSeconds: float


class ExerciseType(BaseModel):
    type: Literal["reps", "duration"]


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

MODEL = "gpt-4o-mini"


def analyse_message(
    message: str, api_key: str
) -> Union[RepsExercise, DurationExercise]:
    client = openai.OpenAI(api_key=api_key)

    # ——— Pass 1: Classify the exercise type
    # .parse() will convert the model’s output directly into your Pydantic class.
    type_model = client.responses.parse(
        model=MODEL,
        input=[
            {
                "role": "system",
                "content": "Classify the exercise as a rep-based exercise or a duration-based exercise.",
            },
            {
                "role": "user",
                "content": message,
            },
        ],
        text_format=ExerciseType,
        temperature=0.0,
    )
    print(f"type_model: {type_model}")
    print(f"type_model.output_parsed: {type_model.output_parsed}")
    # require error handling here.
    ex_type: ExerciseType = type_model.output_parsed
    logger.info("Classified as: %s", ex_type)

    # ——— Pass 2: Extract details with the right schema
    if ex_type.type == "reps":
        exercise = client.responses.parse(
            model=MODEL,
            input=[
                {
                    "role": "system",
                    "content": "Extract the number of reps, and any weight or RIR if mentioned.",
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            text_format=RepsExercise,
            temperature=0.0,
        )
    elif ex_type.type == "duration":
        exercise = client.responses.parse(
            model=MODEL,
            input=[
                {
                    "role": "system",
                    "content": "Extract the duration in seconds, and any weight or RIR if mentioned.",
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            text_format=DurationExercise,
            temperature=0.0,
        )
    else:
        logger.warning("Unknown exercise type: %s", type_model)

    logger.info("Extracted exercise: %s", exercise.output_parsed)
    return exercise.output_parsed


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
    m = update.message
    user = update.effective_user.id if update.effective_user else "unknown"
    if not m.text:
        logger.info("Received non-text message from user %s", user)
        return

    logger.info("Received message from user %s: %r", user, m.text)
    openai_key = os.getenv("OPENAI_KEY")
    exercise = analyse_message(m.text, openai_key)
    await m.reply_text(f"Sentiment analysis:\n{exercise}")
    await react(update, context)
    # Add exercise to database here.
    # Append to a text file in the meantime
    with open("exercise_log.txt", "a") as f:
        f.write(f"{user}: {exercise.model_dump_json()}\n")


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
