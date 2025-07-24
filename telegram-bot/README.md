# ZacTelegramBot

A Telegram bot that uses OpenAI's GPT to parse free-form workout logs into structured exercise entries and store them in JSONL.

## Features

- Accepts text, photo, and voice messages
- Parses workout descriptions (sets, reps, weight) via OpenAI GPT
- Persists parsed entries to `workouts.jsonl`

## Requirements

- Python ≥ 3.11
- python-telegram-bot, openai, pydantic, protobuf, grpcio-tools

## Setup

```bash
cd telegram-bot
uv install
```

Create a `.env` file in this directory with your credentials:

```ini
TELEGRAM_TOKEN=your_telegram_bot_token
OPENAI_KEY=your_openai_api_key
```

**Warning:** Do not commit your `.env` file to version control. If you accidentally expose your keys, rotate them immediately.

## Usage

```bash
uv run main.py
```
## Docker
Build and run the Telegram bot in Docker using the provided `docker-compose.yml`:

```bash
# From the repository root
docker-compose build telegram-bot
docker-compose up -d telegram-bot
```

run:

```bash
docker-compose up -d
```

## Generating gRPC Stubs
Protocol buffers are defined in the top-level `proto/` directory, and Python stubs live in `proto_stubs/`.
To regenerate them, build and run the proto-toolchain container:

```bash
docker build -f ../tools/proto-toolchain/Dockerfile -t proto-toolchain .
docker run --rm \
  -v $(pwd)/../proto:/workspace/proto \
  -v $(pwd)/proto_stubs:/workspace/proto_stubs \
  proto-toolchain \
  bash -c "protoc --proto_path=proto --python_out=proto_stubs --grpc_python_out=proto_stubs proto/telegram_message.proto"
```

After regeneration, commit the updated files under `proto_stubs/`.
