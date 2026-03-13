#!/bin/bash
set -e

echo "Starting Flask application..."
exec gunicorn \
    --bind 0.0.0.0:$PORT \
    --workers 1 \
    --threads 8 \
    --timeout 0 \
    --access-logfile - \
    --error-logfile - \
    --log-level info \
    wsgi:app
