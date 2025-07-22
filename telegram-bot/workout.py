import logging
import openai

from typing import Union, Literal, Optional
from pydantic import BaseModel, Field
from proto_stubs import telegram_message_pb2

# Exercises I want to record
# - Reps - bench press 5x5 80kg, 8 chin-ups, 10 push-ups
# - Duration - 30 minutes running, 15 minutes cycling, 20 minutes rowing

EXERCISE_NAMES = [
    "Bench Press",
    "Chin-Up",
    "Pull-Up",
    "Push-Up",
    "Shoulder Press",
    "Goblet Squat",
    "Deadlift",
    "Farmer's Carry",
]


class ExerciseEntry(BaseModel):
    exerciseName: str
    type: Literal["reps", "duration"]
    reps: Optional[int] = None
    durationInSeconds: Optional[float] = None
    weightInKilograms: Optional[float] = None
    distanceInMeters: Optional[float] = None
    repsInReserve: Optional[int] = None
    notes: Optional[str] = None


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


class WorkoutHandler:
    def __init__(self, OpenAIKey: str):
        self.client = openai.OpenAI(api_key=OpenAIKey)
        self.MODEL = "gpt-4o-mini"

    def handleTelegramMessage(
        self, message: telegram_message_pb2.TelegramMessageV1
    ) -> str:
        exercise = self.__extractExercise(message=message.text)
        logger.info(f"Message: {message}. Exercise is {exercise}")
        # Write the exercise to a log
        with open("workout_log.txt", "a") as f:
            f.write(f"{message.event_id} | {exercise}\n")
        return f"{exercise}"

    def __extractExercise(self, message: str) -> ExerciseEntry:
        system_prompt = str(
            "You are a personal trainer bot that helps users log their workouts. "
            "You will receive messages from users describing their exercises, and you need to extract the relevant details about the exercise. "
            "For example: "
            "'bench press 5x80kg' — this is a reps exercise with 5 reps at 80kg. "
            "'8 chin-ups' — this is a reps exercise with 8 reps. "
            "'30 minutes running' — this is a duration exercise for 30 minutes. "
            "Return the exercise details in the format of ExerciseEntry. "
            "The exercise can be of type 'reps' or 'duration'."
        )

        resp = self.client.responses.parse(
            model=self.MODEL,
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "system",
                    "content": f"Below is a list of exercise names that can be logged: {', '.join(EXERCISE_NAMES)}",
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            text_format=ExerciseEntry,
            temperature=0.0,
        )

        if resp.error:
            raise Exception(resp.error)

        return resp.output_parsed
