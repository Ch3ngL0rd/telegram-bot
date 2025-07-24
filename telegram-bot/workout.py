import logging
import openai

from proto_stubs import telegram_message_pb2
from storage import JsonlWorkoutStore
from exercise import MultipleExerciseEntry

EXERCISE_NAMES = [
    "Bench Press",
    "Chin-Up",
    "Pull-Up",
    "Push-Up",
    "Shoulder Press",
    "Goblet Squat",
    "Deadlift",
    "Farmer's Carry",
    "Running",
]

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


class WorkoutHandler:
    def __init__(self, OpenAIKey: str, store: JsonlWorkoutStore):
        self.client = openai.OpenAI(api_key=OpenAIKey)
        self.MODEL = "gpt-4o-mini"
        self.store = store

    def handleTelegramMessage(
        self, message: telegram_message_pb2.TelegramMessageV1
    ) -> str:
        exercises = self.__extractExercises(message=message.text)
        logger.info(f"Message: {message}. Exercises are {exercises}")
        for exercise in exercises:
            self.store.write(message=message, entry=exercise)
        return f"{exercises}"

    def __extractExercises(self, message: str) -> MultipleExerciseEntry:
        system_prompt = """
            You are a personal trainer bot that helps users log their workouts.
            You will receive messages from users describing their exercises, and you need to extract the relevant details about the exercise.
            For example:
            'bench press 5x80kg' — this is a reps exercise with 5 reps at 80kg.
            '8 chin-ups' — this is a reps exercise with 8 reps.
            '30 minutes running' — this is a duration exercise for 30 minutes.
            Return the exercise details in the format of ExerciseEntry.
            The exercise can be of type 'reps' or 'duration'.
        """

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
            text_format=MultipleExerciseEntry,
            temperature=0.0,
        )

        if resp.error:
            raise Exception(resp.error)

        return resp.output_parsed.exercises
