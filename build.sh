#!/usr/bin/env bash
# exit on error
set -o errexit

# Make sure the script is executable
chmod a+x build.sh

# Install dependencies
pip install -r requirements.txt

# Navigate to the project directory
cd skbulletin

# Create necessary directories with proper permissions
mkdir -p media static data staticfiles
chmod -R 755 media static data staticfiles

# Run database migrations
echo "Running database migrations..."
python manage.py makemigrations bulletin
python manage.py migrate

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
END

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Verify database tables
echo "Verifying database tables..."
python manage.py shell << END
from django.db import connection
tables = connection.introspection.table_names()
print("Available tables:", tables)
END

# Create superuser if needed (uncomment and set env vars to use)
# python manage.py createsuperuser --no-input --username $DJANGO_SUPERUSER_USERNAME --email $DJANGO_SUPERUSER_EMAIL 