# ZacTelegramBot Monorepo

This repository contains the ZacTelegramBot and supporting tools, including a proto toolchain and a Docker Compose setup for running the bot.

## Docker & Docker Compose

A `docker-compose.yml` file is provided to build and run the Telegram bot.

### Build & run only the Telegram bot
```bash
docker-compose build telegram-bot
docker-compose up -d telegram-bot
```

### Build & run all services (Telegram bot)
```bash
docker-compose up -d
```

## Proto Toolchain

To generate or update gRPC stubs for `telegram_message.proto`, use the provided `tools/proto-toolchain` image:

```bash
# Build the proto-toolchain image
docker build -f tools/proto-toolchain/Dockerfile -t proto-toolchain .

# Run protoc to regenerate Python stubs
docker run --rm \
  -v $(pwd)/proto:/workspace/proto \
  -v $(pwd)/telegram-bot/proto_stubs:/workspace/proto_stubs \
  proto-toolchain \
  bash -c "protoc --proto_path=proto --python_out=proto_stubs --grpc_python_out=proto_stubs proto/telegram_message.proto"
```

## Environment Variables

Define the following in `telegram-bot/.env`:

- `TELEGRAM_TOKEN`: Telegram Bot API token
- `OPENAI_KEY`: OpenAI API key