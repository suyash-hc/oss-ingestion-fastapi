FROM python:3.11-alpine

# Install required dependencies and create a non-root user
RUN apk add --no-cache \
    curl \
    bash \
    gcc \
    musl-dev \
    cargo \
    && adduser -D -h /home/oss-ingestion-user -s /bin/bash oss-ingestion-user

WORKDIR /oss-ingestion

# Install virtualenv
RUN python3 -m venv /oss-ingestion/.venv

# Copy application code and install dependencies
COPY app /oss-ingestion/app
COPY main.py /oss-ingestion/main.py
COPY requirements.txt /oss-ingestion/requirements.txt

RUN /oss-ingestion/.venv/bin/pip install --no-cache-dir -r /oss-ingestion/requirements.txt

# Copy startup script
COPY start.sh /oss-ingestion/start.sh
# Make the start.sh script executable and set ownership of the application directory, excluding .venv
RUN chmod +x /oss-ingestion/start.sh && \
    find /oss-ingestion -path /oss-ingestion/.venv -prune -o -exec chown oss-ingestion-user:oss-ingestion-user {} +

# Set environment variables
ENV PATH="/oss-ingestion/.venv/bin:$PATH"
ENV HOST=0.0.0.0
ENV PORT=8000

# Expose the application port
EXPOSE $PORT

# Add a healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:$PORT/ingestion/health || exit 1

# Switch to non-root user
USER oss-ingestion-user

# Use exec form with shell wrapper
CMD ["/oss-ingestion/start.sh"]