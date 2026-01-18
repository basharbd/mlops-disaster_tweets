# 1. Base Image
FROM python:3.10-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy files from your laptop to the container
# We copy requirements first to cache dependencies (makes building faster)
COPY requirements.txt requirements.txt
COPY pyproject.toml pyproject.toml

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Install your own project as a package
COPY src/ src/
RUN pip install --no-cache-dir .

# 5. Open port 8000 so the world can talk to the API
EXPOSE 8000

# 6. Run the server
CMD ["python", "-m", "uvicorn", "src.disaster_tweets.api:app", "--host", "0.0.0.0", "--port", "8000"]
