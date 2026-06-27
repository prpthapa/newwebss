# Notes - Educational Study Platform

A Django-based web application that provides students with access to high-quality handwritten notes for subjects like Physics, Chemistry, and Computer Science.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Django](https://img.shields.io/badge/Django-6.0.2-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## Features

- **Multi-Subject Support** - Organized notes for Physics, Chemistry, Computer Science, and more
- **Hierarchical Structure** - Subjects → Chapters → Topics → Notes
- **Cloudinary Integration** - Cloud-based image storage for note images and thumbnails
- **Responsive Design** - Modern, mobile-friendly UI with AOS animations
- **Admin Dashboard** - Rich Django admin interface with bulk upload capability
- **Contact Form** - Built-in contact form with email notifications
- **View Tracking** - Track note views for analytics
- **CORS Support** - Ready for frontend/backend separation

## Project Structure

```
notes_project/
├── notes_project/          # Django project settings
│   ├── settings.py         # Configuration (DB, Cloudinary, etc.)
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI application
├── notes/                  # Main application
│   ├── models.py           # Subject, Chapter, Topic, Note models
│   ├── views.py            # Page views and API endpoints
│   ├── urls.py             # App URL patterns
│   ├── admin.py            # Admin panel configuration
│   └── bulk_upload.py      # Bulk note upload functionality
├── templates/              # HTML templates
│   ├── base.html           # Base template with header/footer
│   ├── index.html          # Homepage
│   ├── subject_detail.html # Subject listing page
│   ├── chapter_detail.html # Chapter listing page
│   └── topic_detail.html   # Notes viewing page
├── static/                 # Static files (CSS, JS, images)
├── media/                  # Uploaded media files
├── manage.py               # Django management script
└── requirements.txt        # Python dependencies
```

## Data Models

| Model | Description |
|-------|-------------|
| `Subject` | Top-level subject (e.g., Physics, Chemistry) with preview image and icon |
| `Chapter` | Chapters within a subject with thumbnails and ordering |
| `Topic` | Topics within a chapter with thumbnails |
| `Note` | Individual note images with page numbers and view counts |
| `ContactMessage` | Contact form submissions |

## Installation

### Prerequisites

- Python 3.12+
- PostgreSQL (or SQLite for development)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd notes_project
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file** (optional for local dev — defaults work when `DEBUG=True`)
   ```bash
   cp .env.example .env
   # Edit .env and replace the placeholders with real values.
   # Generate a SECRET_KEY with:
   #   python -c "import secrets; print(secrets.token_urlsafe(50))"
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Homepage: http://localhost:8000
   - Admin panel: http://localhost:8000/admin

## Deployment

### Production Server

The project uses **Gunicorn** as the WSGI server and **WhiteNoise** for static file serving.

```bash
# Install production dependencies
pip install -r requirements.txt

# Run with Gunicorn
gunicorn notes_project.wsgi:application
```

### Deploying to Render

The repository includes a `render.yaml` Blueprint and a `build.sh` script. To deploy:

1. In the Render dashboard: **New** → **Blueprint** → connect this repo.
2. Render will create the Postgres database and web service automatically.
3. On first deploy, Render auto-generates `SECRET_KEY`, `STUDIO_USERNAME`, and `STUDIO_PASSWORD`. Change the studio credentials in the web service's **Environment** tab to values you choose.
4. Create a Django admin user once via the Render shell:
   ```bash
   python manage.py createsuperuser
   ```

The default gunicorn config (see `gunicorn.conf.py`) honours Render's `PORT` env var and runs 3 workers on the free tier. Logs stream to stdout, which Render's log drainer captures.

### Rotate the historical SECRET_KEY

> **Heads up:** an older version of this repository had a real-looking `SECRET_KEY` value committed to `.env` for local development. If you forked/cloned the project before the hardening PR, rotate the key:
>
> 1. Generate a fresh one: `python -c "import secrets; print(secrets.token_urlsafe(50))"`
> 2. Set it in Render's env-var UI (the `SECRET_KEY` row will be regenerated automatically on the next deploy, but you can paste your own value to keep it stable).
> 3. Any existing sessions, password reset links, or signed cookies will be invalidated — that's expected.

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/contact/` | POST | Submit contact form |
| `/api/note/<id>/view/` | POST | Increment note view count |

## Admin Features

- **Rich Admin Interface** - Custom admin views with image previews
- **Bulk Upload** - Upload multiple notes at once via `/admin/bulk-upload-notes/`
- **Inline Editing** - Edit chapters within subjects, topics within chapters

## Technology Stack

- **Backend**: Django 6.0.2, Django REST Framework 3.16.1
- **Database**: PostgreSQL (production), SQLite (development)
- **Static Files**: WhiteNoise
- **Server**: Gunicorn
- **Frontend**: HTML5, CSS3, JavaScript, AOS Animations, Font Awesome

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues and questions:
- Create an issue on GitHub
- Contact: pdpthapa1515@gmail.com
