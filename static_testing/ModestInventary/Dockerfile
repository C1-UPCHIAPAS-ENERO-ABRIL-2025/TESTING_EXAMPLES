# Dockerfile with intentional bad practices for Hadolint to catch.

# DL3007: Using latest is not recommended
FROM python:latest

# Set a working directory
WORKDIR /app

# DL3042, DL3013: Copying everything and not using --no-cache-dir
COPY . .
RUN pip install -r requirements.txt

# Default command to run the CLI
CMD ["python", "-m", "inventory_system.cli"]