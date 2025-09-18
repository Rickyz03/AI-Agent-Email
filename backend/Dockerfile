# Backend Dockerfile
FROM python:3.13-slim

# Set timezone
ENV TZ=Europe/Rome

WORKDIR /

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    tzdata \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the backend
COPY . .

# Expose port
EXPOSE 8001

# Start with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001", "--reload"]
