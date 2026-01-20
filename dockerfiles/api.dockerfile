FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything needed into the /app folder
COPY static/ /app/static/
COPY models/ /app/models/
COPY src/disaster_tweets/ /app/disaster_tweets/
# Also copy the files into the root of /app to make imports easy
COPY src/disaster_tweets/*.py /app/

# Set the working directory to where the code is
ENV PYTHONPATH=/app
ENV PORT=8080

EXPOSE 8080

# Start the app
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
