# Use official Python slim image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

# Install system dependencies in a single RUN step to reduce layers,
# and clean up afterwards to minimize image size
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files last to utilize Docker cache more efficiently for dependencies
COPY . .

# Set user to non-root for security (recommended)
RUN adduser --disabled-password myuser
USER myuser

# Expose port (optional: for documentation purposes)
EXPOSE 8000

# Command to run Gunicorn
CMD ["gunicorn", "autoai_email.wsgi:application", "--bind", "0.0.0.0:8000"]