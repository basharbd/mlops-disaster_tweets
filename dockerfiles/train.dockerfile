# Use a lightweight Python base image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install git (needed for some dependencies)
RUN apt-get update && apt-get install -y git

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY src/ src/

# Set the Python path so it finds your modules
ENV PYTHONPATH=/app/src

# The command to run when the container starts
CMD ["python", "src/disaster_tweets/train.py"]
