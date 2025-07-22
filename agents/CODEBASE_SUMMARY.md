 # Codebase Summary

 This repository implements a Telegram bot named "ZacTelegramBot" that leverages OpenAI's GPT to parse users' workout logs and store them as structured data.

 ## Repository Layout

 ```
 .
 ├── .github/                # GitHub Actions workflows (CI/CD)
 ├── proto/                  # Protobuf definitions for Telegram messages
 ├── tools/
 │   └── proto-toolchain/    # Dockerfile for building/generating protobuf stubs
 └── telegram-bot/
     ├── proto_stubs/        # Generated Python gRPC/protobuf stubs
     ├── main.py             # Bot entrypoint with Telegram handlers
     ├── exercise.py         # Pydantic model for structured exercise data
     ├── workout.py          # Core workout parsing logic using OpenAI
     ├── storage.py          # JSONL storage for workout entries
     ├── pyproject.toml      # Project configuration & dependencies
     └── workouts.jsonl      # Persisted workout logs (created at runtime)
 ```

 ## Core Components

 ### `proto/telegram_message.proto`
 Defines the `TelegramMessageV1` message with fields for event ID, timestamp, chat/user IDs, media kind, text content, and file pointers.

 ### `telegram-bot/main.py`
 - Sets up the bot with `/start` and a message handler for text, photo, and voice.
 - `ingest()` constructs `TelegramMessageV1` proto messages, invokes the workout handler, reacts with an emoji, and replies to the user.

### `telegram-bot/exercise.py`
- Defines a Pydantic `ExerciseEntry` model for structured exercise data.

### `telegram-bot/workout.py`
- Imports `ExerciseEntry` from `exercise.py` and implements `WorkoutHandler` which calls OpenAI to parse freeform workout descriptions into `ExerciseEntry`.

 ### `telegram-bot/storage.py`
 - Implements `JsonlWorkoutStore` to append parsed entries to a JSONL file (`workouts.jsonl`).

 ### `telegram-bot/proto_stubs/`
 Generated Python classes from the proto definitions; used to serialize/deserialize `TelegramMessageV1`.

 ## Runtime Flow

 1. User sends a message to the bot.
 2. Bot wraps message in a protobuf `TelegramMessageV1`.
 3. `WorkoutHandler` uses GPT to extract structured exercise data.
 4. Parsed entry is logged to `workouts.jsonl`.
 5. Bot reacts with a thumbs up and returns a summary to the user.

 ## Dependencies & Environment

 - Python 3.x
 - `python-telegram-bot`, `openai`, `pydantic`, `protobuf`, `grpcio-tools`
 - Environment variables:
   - `TELEGRAM_TOKEN` – Telegram Bot token
   - `OPENAI_KEY` – OpenAI API key

 ---

 *This summary was generated and stored for future code agents to reference the high-level architecture and flow of the Telegram bot.* 