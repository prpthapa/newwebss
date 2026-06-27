# Notes - Educational Platform Backend

A Django-based backend system for managing and displaying educational notes across multiple subjects.

## Features

✨ **Key Features:**
- 📚 Multi-subject support (Physics, Chemistry, Computer Science, etc.)
- 📖 Chapter-based organization
- 🖼️ Image-based note display with viewer features
- 👨‍💼 Comprehensive Django Admin panel
- 📱 Responsive design
- 🔍 View counter for notes
- 🎨 Customizable subject themes and icons
- 📧 Contact form functionality

## Project Structure

```
notes_project/
├── config/                 # Django project settings
│   ├── __init__.py
│   ├── settings.py        # Main settings
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI config
│   └── asgi.py            # ASGI config
├── notes_app/             # Main application
│   ├── migrations/        # Database migrations
│   ├── static/            # Static files (CSS, JS, images)
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/         # HTML templates
│   │   └── notes_app/
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # App URL patterns
│   ├── admin.py           # Admin configuration
│   └── apps.py            # App configuration
├── templates/             # Base templates
│   └── base.html
├── media/                 # Uploaded files
│   ├── subjects/          # Subject preview images
│   ├── chapters/          # Chapter thumbnails
│   └── note_images/       # Note page images
├── manage.py              # Django management script
└── requirements.txt       # Python dependencies
```

## Database Models

### Subject
- Name, slug, description
- Preview image and icon
- Color theme
- Display order
- Active status

### Chapter
- Belongs to a Subject
- Chapter number and title
- Description and thumbnail
- Slug for URLs

### Note
- Belongs to a Chapter
- Page number and title
- Image file
- Description
- View counter

### ContactMessage
- Contact form submissions
- Name, email, subject, message
- Read status

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install required packages
pip install -r requirements.txt
```

### Step 2: Database Setup

```bash
# Create database migrations
python manage.py makemigrations

# Apply migrations to create database tables
python manage.py migrate
```

### Step 3: Create Admin User

```bash
# Create a superuser account for admin access
python manage.py createsuperuser

# Follow the prompts to set:
# - Username
# - Email
# - Password
```

### Step 4: Run Development Server

```bash
python manage.py runserver

# Server will start at: http://127.0.0.1:8000/
# Admin panel: http://127.0.0.1:8000/admin/
```

## Admin Panel Usage

### Accessing Admin Panel
1. Navigate to `http://127.0.0.1:8000/admin/`
2. Login with your superuser credentials

### Adding Content

#### 1. Add Subjects
- Go to **Subjects** in admin
- Click **Add Subject**
- Fill in:
  - Name (e.g., "Physics")
  - Description
  - Upload preview image
  - Set icon class (FontAwesome icons, e.g., "fas fa-atom")
  - Set color theme (hex code, e.g., "#4A90E2")
  - Set display order
  - Mark as active
- Save

#### 2. Add Chapters
- Go to **Chapters** in admin
- Click **Add Chapter**
- Fill in:
  - Select subject
  - Chapter number
  - Title
  - Description
  - Upload thumbnail (optional)
  - Mark as active
- Save

#### 3. Add Notes
- Go to **Notes** in admin
- Click **Add Note**
- Fill in:
  - Select chapter
  - Page number
  - Title
  - Upload note image
  - Add description (optional)
  - Mark as active
- Save

**Tip:** You can also add notes directly from the Chapter edit page using inline forms!

### Managing Content

#### Bulk Operations
- Use checkboxes to select multiple items
- Use action dropdown for bulk operations
- Mark items as active/inactive

#### Filtering
- Use right sidebar filters to find content by:
  - Subject
  - Active status
  - Creation date

#### Searching
- Use search bar to find content by name, title, or description

## URL Structure

```
/                                          # Home page
/subject/<slug>/                           # Subject detail (list of chapters)
/subject/<slug>/chapter/<slug>/            # Chapter detail (notes viewer)
/contact/                                  # Contact form
/admin/                                    # Admin panel
```

## Configuration

### Settings (`config/settings.py`)

Key settings you might want to modify:

```python
# Security
SECRET_KEY = 'your-secret-key-here'  # Change in production!
DEBUG = True                          # Set to False in production
ALLOWED_HOSTS = ['*']                 # Restrict in production

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
```

### Production Deployment

Before deploying to production:

1. **Change SECRET_KEY**:
   ```python
   import secrets
   SECRET_KEY = secrets.token_urlsafe(50)
   ```

2. **Disable DEBUG**:
   ```python
   DEBUG = False
   ```

3. **Set ALLOWED_HOSTS**:
   ```python
   ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
   ```

4. **Collect static files**:
   ```bash
   python manage.py collectstatic
   ```

5. **Use production database** (PostgreSQL recommended):
   ```python
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'your_db_name',
           'USER': 'your_db_user',
           'PASSWORD': 'your_db_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }
   ```

## Features Breakdown

### Frontend Features
- **Responsive Design**: Works on all devices
- **Smooth Animations**: AOS library integration
- **Image Viewer**: 
  - Scroll, grid, and slideshow modes
  - Zoom controls
  - Fullscreen view
  - Keyboard navigation
- **Chapter Navigation**: Easy prev/next navigation
- **View Counter**: Tracks note popularity

### Admin Features
- **Rich Admin Interface**: 
  - Image previews
  - Inline editing
  - Bulk operations
  - Advanced filtering
- **Statistics**: 
  - Chapter count per subject
  - Note count per chapter
  - View counts per note
- **Media Management**: Automatic file organization
- **Validation**: Unique slugs and ordering

## Customization

### Adding New Subject Icons
Use FontAwesome 6 icon classes:
```
fas fa-atom          # Physics
fas fa-flask         # Chemistry
fas fa-laptop-code   # Computer Science
fas fa-calculator    # Mathematics
fas fa-dna           # Biology
```

### Changing Color Themes
Use hex color codes in Subject admin:
```
#4A90E2  # Blue
#E74C3C  # Red
#2ECC71  # Green
#F39C12  # Orange
#9B59B6  # Purple
```

## Troubleshooting

### Static files not loading
```bash
python manage.py collectstatic
```

### Database errors after model changes
```bash
python manage.py makemigrations
python manage.py migrate
```

### Admin styles not working
Make sure you've run:
```bash
python manage.py collectstatic --noinput
```

### Images not displaying
1. Check MEDIA_ROOT and MEDIA_URL settings
2. Ensure debug mode is on or configure web server for media files
3. Verify file permissions on media directory

## Development Tips

### Adding Custom Management Commands
Create `notes_app/management/commands/` directory and add commands

### Database Backup
```bash
# SQLite
python manage.py dumpdata > backup.json

# Restore
python manage.py loaddata backup.json
```

### Testing
```bash
python manage.py test notes_app
```

## Support

For issues or questions:
1. Check Django documentation: https://docs.djangoproject.com/
2. Review code comments in models.py and views.py
3. Check admin panel configuration in admin.py

## License

This project is created for educational purposes.

## Credits

- Django Web Framework
- FontAwesome Icons
- AOS Animation Library
- Pillow (Python Imaging Library)
