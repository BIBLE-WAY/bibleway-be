#!/bin/sh

echo "Starting BibleWay Backend..."

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Create index for Elasticsearch (optional - will fail silently if ES not ready)
echo "Indexing Elasticsearch (if available)..."
python manage.py index_chapters || echo "Elasticsearch indexing skipped"

echo "Setup complete!"

# Get port (default to 8080 if not set)
PORT="${PORT:-8080}"

echo "Starting Gunicorn server on port $PORT..."

# Start Gunicorn server
exec gunicorn bible_way_backend.wsgi:application \
    --bind "0.0.0.0:$PORT" \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --access-logfile - \
    --error-logfile -
