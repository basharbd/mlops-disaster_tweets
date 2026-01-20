FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# 1. Install dependencies first (for better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytorch-lightning

# 2. Copy the whole project including setup.py and src/
COPY . .

# 3. Install the project itself as a package
RUN pip install -e .

EXPOSE 8080

# Use the full package path to start the app
CMD ["uvicorn", "disaster_tweets.api:app", "--host", "0.0.0.0", "--port", "8080"]
