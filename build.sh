#!/usr/bin/env bash
# exit on error
set -o errexit

# Make sure the script is executable
chmod a+x build.sh

# Install dependencies
pip install -r requirements.txt

# Navigate to the project directory
cd skbulletin

# Create necessary directories
mkdir -p media
mkdir -p data

# Move to a persistent directory if it doesn't exist
if [ ! -f "data/db.sqlite3" ]; then
    python manage.py migrate --no-input
    python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END
    # Move the database to the persistent directory
    mv db.sqlite3 data/db.sqlite3
fi

# Collect static files
python manage.py collectstatic --no-input

# Create superuser if needed (uncomment and set env vars to use)
# python manage.py createsuperuser --no-input --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL 