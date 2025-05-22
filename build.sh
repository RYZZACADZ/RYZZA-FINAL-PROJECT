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
mkdir -p staticfiles

# Always run migrations
python manage.py migrate --no-input

# Create superuser if it doesn't exist
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END

# Collect static files
python manage.py collectstatic --no-input --clear

# Ensure proper permissions
chmod -R 755 media
chmod -R 755 data
chmod -R 755 staticfiles

# Create superuser if needed (uncomment and set env vars to use)
# python manage.py createsuperuser --no-input --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL 