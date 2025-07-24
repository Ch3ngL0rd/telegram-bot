# Dockerfile for ZacTelegramBot
FROM python:3.11-slim

# Install uv tool to manage dependencies
RUN pip install --no-cache-dir uv

WORKDIR /app

# Copy project metadata and lock file for dependency installation
COPY requirements.txt ./

# Install Python dependencies into isolated venv
RUN uv pip install --system --requirements requirements.txt

# Copy application code
COPY . .

# Expose ports if using gRPC or metrics, e.g., 50051 for gRPC
# EXPOSE 50051

# Default command: run the bot
CMD ["uv", "run", "main.py"]
