import json


from proto_stubs.telegram_message_pb2 import TelegramMessageV1
from exercise import ExerciseEntry


class JsonlWorkoutStore:
    """
    Stores workout entries as JSON lines.
    """
    def __init__(self, filename: str):
        self.filename = filename

    def write(self, message: TelegramMessageV1, entry: ExerciseEntry) -> None:
        record = {
            "event_id": message.event_id,
            "user_id": message.user_id,
            "chat_id": message.chat_id,
            "ts": message.ts.ToJsonString(),
            "exercise": entry.model_dump(),
        }
        with open(self.filename, "a") as f:
            f.write(json.dumps(record))
            f.write("\n")