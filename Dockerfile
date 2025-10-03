# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m appuser
WORKDIR /app

# System deps (for gTTS/pyowm no extras are needed, but keep tools for builds)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Container-side port used by webserver.keep_alive() (Flask dev server)
EXPOSE 8080

# Start the Telegram bot (which also spins up the keep-alive Flask thread)
CMD ["python", "app.py"]
