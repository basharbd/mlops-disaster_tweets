FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir pytorch-lightning

COPY . .

# Register the package
RUN pip install -e .

# Run as a module so imports inside train.py work correctly
CMD ["python", "-m", "disaster_tweets.train"]
