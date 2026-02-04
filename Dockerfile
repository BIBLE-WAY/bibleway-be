# BibleWay Backend Dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=bible_way_backend.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create staticfiles directory
RUN mkdir -p /app/staticfiles

# Collect static files during build
RUN python manage.py collectstatic --noinput || true

# Expose port
EXPOSE 8080

# Start command - Railway will inject PORT
CMD python manage.py migrate --noinput && gunicorn bible_way_backend.wsgi:application --bind 0.0.0.0:8080 --workers 2 --threads 4 --timeout 120
