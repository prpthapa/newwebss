from django.db import models
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator


class Subject(models.Model):
    """
    Model for subjects like Physics, Chemistry, Computer Science
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(help_text="Brief description of the subject")
    preview_image = models.ImageField(
        upload_to='subjects/',
        blank=True,
        null=True,
        help_text="Preview image for the subject card (PNG, JPG, SVG)"
    )
    icon_class = models.CharField(
        max_length=50,
        default='fas fa-book',
        help_text="Font Awesome icon class (e.g., 'fas fa-atom')"
    )
    order = models.IntegerField(
        default=0,
        help_text="Order in which subjects appear (lower numbers first)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_chapters_count(self):
        return self.chapters.filter(is_active=True).count()

    def get_notes_count(self):
        total = 0
        for chapter in self.chapters.filter(is_active=True):
            for topic in chapter.topics.filter(is_active=True):
                total += topic.notes.filter(is_active=True).count()
        return total


class Chapter(models.Model):
    """
    Model for chapters within a subject
    """
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='chapters'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    chapter_number = models.IntegerField(
        help_text="Chapter number for ordering (e.g., 1, 2, 3)"
    )
    thumbnail = models.ImageField(
        upload_to='chapters/',
        blank=True,
        null=True,
        help_text="Thumbnail image for the chapter (PNG, JPG, SVG)"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['chapter_number', 'title']
        verbose_name = 'Chapter'
        verbose_name_plural = 'Chapters'
        unique_together = ['subject', 'chapter_number']

    def __str__(self):
        return f"{self.subject.name} - Chapter {self.chapter_number}: {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.chapter_number}-{self.title}")
        super().save(*args, **kwargs)

    def get_topics_count(self):
        return self.topics.filter(is_active=True).count()

    def get_notes_count(self):
        total = 0
        for topic in self.topics.filter(is_active=True):
            total += topic.notes.filter(is_active=True).count()
        return total


class Topic(models.Model):
    """
    Model for topics within a chapter
    """
    chapter = models.ForeignKey(
        Chapter,
        on_delete=models.CASCADE,
        related_name='topics'
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    topic_number = models.IntegerField(
        help_text="Topic number for ordering (e.g., 1, 2, 3)"
    )
    thumbnail = models.ImageField(
        upload_to='topics/',
        blank=True,
        null=True,
        help_text="Thumbnail image for the topic"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['topic_number', 'title']
        verbose_name = 'Topic'
        verbose_name_plural = 'Topics'
        unique_together = ['chapter', 'topic_number']

    def __str__(self):
        return f"{self.chapter.title} - Topic {self.topic_number}: {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.topic_number}-{self.title}")
        super().save(*args, **kwargs)

    def get_notes_count(self):
        return self.notes.filter(is_active=True).count()


class Note(models.Model):
    """
    Model for individual note images within a topic
    """
    topic = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='notes'
    )
    title = models.CharField(
        max_length=200,blank=True,
        help_text="Title or description of the note"
    )
    image = models.ImageField(
        upload_to='notes/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'webp'])],
        help_text="Upload note image (JPG, PNG, or WebP)"
    )
    page_number = models.IntegerField(
        help_text="Page/sequence number for ordering"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description or topics covered in this note"
    )
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['page_number', 'created_at']
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
        unique_together = ['topic', 'page_number']

    def __str__(self):
        return f"{self.topic.chapter.subject.name} - {self.topic.title} - Page {self.page_number}"

    def increment_views(self):
        self.views += 1
        self.save(update_fields=['views'])


class ContactMessage(models.Model):
    """
    Model for storing contact form submissions
    """
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.name} - {self.subject}"
