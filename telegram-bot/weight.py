import logging
import openai

from exercise import WeightEntry
from proto_stubs import telegram_message_pb2

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)


class WeightHandler:
    def __init__(self, openai_key: str, weight_store: JsonlWorkoutStore):
        self.client = openai.OpenAI(api_key=openai_key)
        self.MODEL = "gpt-4o-mini"

    def handleWeightMessage(
        self, message: telegram_message_pb2.TelegramMessageV1
    ) -> str:
        weight = self.__extractWeightDetails(message.text)
        if message.ts:
            weight.ts = message.ts.ToJsonString()
        logger.info(f"Message: {message}. Weight details are {weight}")
        return f"Weight logged: {weight.weightInKilograms} kg"

    def __extractWeightDetails(self, message: str) -> WeightEntry:
        system_prompt = """
            You are a weight management bot that helps users log their weight.
            You will receive messages from users describing their weight, and you need to extract the relevant details.
            For example:
            'I weigh 70kg' — this is a weight entry of 70kg.
            'My current weight is 75.5kg' — this is a weight entry of 75.5kg.
            Return the weight details in a dictionary format.
        """

        resp = self.client.responses.parse(
            model=self.MODEL,
            input=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            text_format=WeightEntry,
            temperature=0.0,
        )

        if resp.error:
            raise Exception(resp.error)

        return resp.output_parsed
