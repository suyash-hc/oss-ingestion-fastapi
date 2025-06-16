#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

# Default values if not set
HOST=${HOST:-0.0.0.0}
PORT=${PORT:-8000}

# Debug logging
echo "Starting application on HOST=$HOST and PORT=$PORT"

# Check if uvicorn is installed
if ! command -v uvicorn >/dev/null 2>&1; then
    echo "Error: uvicorn is not installed." >&2
    exit 1
fi

# Check if the application entry point exists
if [ ! -f main.py ]; then
    echo "Error: Application entry point 'main:app' not found." >&2
    exit 1
fi

# Start the FastAPI application
exec uvicorn main:app --host "$HOST" --port "$PORT"