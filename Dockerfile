FROM python:3.12-slim

# Create application and default output directory
WORKDIR /app

# Copy generator source and default fallback flag
COPY src/ /app/src/
COPY flag.txt /app/flag.txt

# Ensure output directory exists and is writable by any UID (dynamic container runner may run as arbitrary non-root user)
RUN mkdir -p /output && chmod 777 /output

# Default environment settings
ENV OUTPUT_DIR=/output \
    OUTPUT_FILENAME=message.txt

# Entrypoint runs the dynamic file generator
ENTRYPOINT ["python3", "/app/src/generate.py"]
