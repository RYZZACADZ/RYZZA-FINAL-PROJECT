#!/usr/bin/env bash
# exit on error
set -o errexit

echo "Starting build process..."

# Make sure the script is executable
chmod a+x build.sh

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Navigate to the project directory
cd skbulletin

# Create necessary directories with proper permissions
echo "Creating necessary directories..."
mkdir -p media/announcement_images
mkdir -p media/event_images
mkdir -p media/alert_images
mkdir -p static/css
mkdir -p static/js
mkdir -p static/images
mkdir -p static/fonts
mkdir -p data
mkdir -p staticfiles
mkdir -p bulletin/static/css
mkdir -p bulletin/static/js
mkdir -p bulletin/static/images
mkdir -p bulletin/static/fonts

# Set proper permissions
echo "Setting permissions..."
chmod -R 755 media
chmod -R 755 static
chmod -R 755 data
chmod -R 755 staticfiles
chmod -R 755 bulletin/static

# Database migrations
echo "Running database migrations..."
python manage.py migrate auth
python manage.py migrate admin
python manage.py migrate contenttypes
python manage.py migrate sessions
python manage.py makemigrations bulletin
python manage.py migrate bulletin
python manage.py migrate

# Verify database tables
echo "Verifying database tables..."
python manage.py shell << END
from django.db import connection
from bulletin.models import Announcement, Event, EmergencyAlert, Feedback, Contact
tables = connection.introspection.table_names()
print("Available tables:", tables)
models = [Announcement, Event, EmergencyAlert, Feedback, Contact]
for model in models:
    table_name = model._meta.db_table
    if table_name in tables:
        print(f"✓ Table {table_name} exists")
    else:
        print(f"✗ Table {table_name} is missing")
        # If table is missing, show the expected SQL
        from django.db import connection
        from django.db.migrations.executor import MigrationExecutor
        executor = MigrationExecutor(connection)
        plan = executor.migration_plan([(model._meta.app_label, None)])
        if plan:
            print("Migration plan exists for", table_name)
        else:
            print("No migration plan found for", table_name)
END

# Create superuser if it doesn't exist
echo "Creating superuser..."
python manage.py shell << END
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print("✓ Superuser created successfully")
else:
    print("✓ Superuser already exists")
END

# Copy static files
echo "Copying static files..."
cp -r bulletin/static/* static/ 2>/dev/null || true

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input --clear

# Final verification
echo "Final verification..."
python manage.py check --deploy

echo "Build completed successfully!" 