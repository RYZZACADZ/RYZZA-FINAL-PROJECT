# SK Bulletin System

A web-based bulletin system for Sangguniang Kabataan to manage and display announcements, events, and emergency alerts.

## Features

- Event Management with Status Tracking
- Announcement System
- Emergency Alert System
- User Authentication
- Responsive Design
- API Endpoints

## Tech Stack

- Django 5.0
- Bootstrap 5
- PostgreSQL (Production)
- SQLite (Development)
- Whitenoise for static files
- Gunicorn for production server

## Local Development Setup

1. Clone the repository:
```bash
git clone https://github.com/RYZZACADZ/RYZZA-FINAL-PROJECT.git
cd RYZZA-FINAL-PROJECT
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Setup environment variables:
Create a `.env` file in the root directory with:
```
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
```

5. Run migrations:
```bash
cd skbulletin
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

## Deployment

This project is configured for deployment on Render.

### Environment Variables for Production

Set these in your Render dashboard:
- `DEBUG`: False
- `SECRET_KEY`: [Generate a secure key]
- `ALLOWED_HOSTS`: your-app.onrender.com
- `DATABASE_URL`: [Provided by Render]
- `SECURE_SSL_REDIRECT`: True

### Deployment Steps

1. Push to GitHub
2. Connect your Render account
3. Create a new Web Service
4. Use the following settings:
   - Build Command: `./build.sh`
   - Start Command: `cd skbulletin && gunicorn skbulletin.wsgi:application`

## License

MIT License 