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
