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
