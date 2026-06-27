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
notes_project/                  # Repo root
├── manage.py                  # Django CLI
├── requirements.txt           # Pinned dependencies (Django, Pillow, …)
├── gunicorn.conf.py           # Production WSGI config (Render)
├── build.sh                   # Render build step
├── render.yaml                # Render Blueprint (defines web service + DB)
├── Procfile                   # Alternative start command
├── .env                       # Local secrets (gitignored)
├── notes_project/             # Django settings package
│   ├── settings.py            # 12-factor settings, env-driven
│   ├── urls.py                # Root URLconf; mounts admin/, studio/, /
│   ├── wsgi.py / asgi.py
│   ├── views.py               # 404/500 handlers + legal pages
│   ├── health.py              # /healthz/ (no DB access)
│   └── media_serve.py         # Production media serving (WhiteNoise handles static)
├── notes/                     # Single Django app
│   ├── models.py              # Subject → Chapter → Topic → Note + ContactMessage
│   ├── views.py               # Public page views + API endpoints
│   ├── studio_views.py        # Private /studio/ views (login-gated) + bulk_create_notes
│   ├── studio_auth.py         # Studio session gate + IP lockout
│   ├── studio_forms.py        # Studio forms (bulk upload, CRUD)
│   ├── studio_urls.py         # /studio/ URLconf
│   ├── forms.py               # Public ContactForm
│   ├── admin.py               # Django admin registration
│   ├── urls.py                # Public URLconf
│   ├── apps.py
│   ├── management/commands/   # bulk_upload_notes (folder import CLI)
│   ├── migrations/
│   └── tests/                 # Smoke tests (health, pages, contact, studio auth)
├── templates/                 # Project-wide templates
│   ├── base.html, 404.html, 500.html, privacy_policy.html, terms.html
│   └── studio/                # studio/{login,dashboard,upload,new_node}.html
├── static/                    # Source assets (CSS, JS, images)
├── staticfiles/               # collectstatic output (gitignored)
└── media/                     # User uploads (gitignored)
```

## Database Models

### Subject
- Name, slug, description
- Preview image and icon
- Display order
- Active status

### Chapter
- Belongs to a Subject
- Chapter number and title
- Description and thumbnail
- Slug for URLs

### Topic
- Belongs to a Chapter
- Topic number and title
- Description and thumbnail
- Slug for URLs

### Note
- Belongs to a Topic
- Page number and title
- Image file
- Description
- View counter

### ContactMessage
- Contact form submissions
- Name, email, subject, message
- Read status


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
