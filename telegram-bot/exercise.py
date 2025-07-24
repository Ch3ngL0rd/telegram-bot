from typing import Literal, Optional
from pydantic import BaseModel


class ExerciseEntry(BaseModel):
    exerciseName: str
    type: Literal["reps", "duration"]
    reps: Optional[int] = None
    durationInSeconds: Optional[float] = None
    weightInKilograms: Optional[float] = None
    distanceInMeters: Optional[float] = None
    repsInReserve: Optional[int] = None
    notes: Optional[str] = None


class MultipleExerciseEntry(BaseModel):
    exercises: list[ExerciseEntry]


class WeightEntry(BaseModel):
    weightInKilograms: float
    ts: Optional[str] = None
    notes: Optional[str] = None
