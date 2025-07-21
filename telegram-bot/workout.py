# What is passed between the telegram and workout?
# TelegramMessageV1
# Given a TelegramMessageV1, workout calls LLM and stores shit.

import logging
import openai

from typing import Union, Literal, Optional
from pydantic import BaseModel, Field
from proto_stubs import telegram_message_pb2

class ExerciseType(BaseModel):
    type: Literal["reps", "duration","unknown"]

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

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

class WorkoutHandler:
    def __init__(self, OpenAIKey: str):
        self.client = openai.OpenAI(api_key=OpenAIKey)
        self.MODEL = "gpt-4o-mini"
    
    def handleTelegramMessage(self, message: telegram_message_pb2.TelegramMessageV1) -> str:
        exerciseType = self.__determineExerciseType(message.text)
        exercise = self.__extractExercise(message=message.text, exerciseType = exerciseType)
        logger.info(f"Message: {message}. Exercise is {exercise}")
        # Write the exercise to a log
        with open("workout_log.txt", "a") as f:
            f.write(f"{message.event_id} | {exercise}\n")
        return f"{exercise}"

    def __determineExerciseType(self, message:str) -> ExerciseType:
        resp = self.client.responses.parse(
            model=self.MODEL,
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

        if resp.error:
            raise Exception(resp.error)

        return resp.output_parsed
    
    def __extractExercise(self, message: str, exerciseType: ExerciseType) -> Union[RepsExercise, DurationExercise]:
        if exerciseType.type == "unknown":
            raise Exception(f"Unknown exercise type: {exerciseType.type}")
        
        model = None
        if exerciseType.type == "duration":
            model = DurationExercise
        elif exerciseType.type == "reps":
            model = RepsExercise

        resp = self.client.responses.parse(
            model=self.MODEL,
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
            text_format=model,
            temperature=0.0,
        )

        if resp.error:
            raise Exception(resp.error)
        
        return resp.output_parsed
