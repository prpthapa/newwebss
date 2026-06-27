from django.contrib import admin
from django.utils.html import format_html
from django.db.models import Count
from .models import Subject, Chapter, Topic, Note, ContactMessage


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'preview_thumbnail', 'chapters_count', 'notes_count', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order', 'is_active']
    readonly_fields = ['created_at', 'updated_at', 'preview_thumbnail']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'icon_class')
        }),
        ('Display Settings', {
            'fields': ('preview_image', 'preview_thumbnail', 'order', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def preview_thumbnail(self, obj):
        if obj.preview_image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 8px;" />',
                obj.preview_image.url
            )
        return "No image"
    preview_thumbnail.short_description = 'Preview'

    def chapters_count(self, obj):
        return obj.get_chapters_count()
    chapters_count.short_description = 'Chapters'

    def notes_count(self, obj):
        return obj.get_notes_count()
    notes_count.short_description = 'Total Notes'


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1
    fields = ['topic_number', 'title', 'is_active']
    ordering = ['topic_number']


@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['chapter_info', 'subject', 'chapter_number', 'thumbnail_preview', 'topics_count', 'notes_count', 'is_active', 'created_at']
    list_filter = ['subject', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'subject__name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at', 'thumbnail_preview']
    inlines = [TopicInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('subject', 'chapter_number', 'title', 'slug', 'description')
        }),
        ('Display Settings', {
            'fields': ('thumbnail', 'thumbnail_preview', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def chapter_info(self, obj):
        return f"Chapter {obj.chapter_number}: {obj.title}"
    chapter_info.short_description = 'Chapter'

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="150" height="100" style="object-fit: cover; border-radius: 8px;" />',
                obj.thumbnail.url
            )
        return "No thumbnail"
    thumbnail_preview.short_description = 'Thumbnail'

    def topics_count(self, obj):
        return obj.get_topics_count()
    topics_count.short_description = 'Topics'

    def notes_count(self, obj):
        return obj.get_notes_count()
    notes_count.short_description = 'Notes'


class NoteInline(admin.TabularInline):
    model = Note
    extra = 1
    fields = ['page_number', 'title', 'image', 'is_active']
    ordering = ['page_number']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['topic_info', 'chapter', 'subject_name', 'topic_number', 'thumbnail_preview', 'notes_count', 'is_active', 'created_at']
    list_filter = ['chapter__subject', 'chapter', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'chapter__title', 'chapter__subject__name']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at', 'thumbnail_preview']
    inlines = [NoteInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('chapter', 'topic_number', 'title', 'slug', 'description')
        }),
        ('Display Settings', {
            'fields': ('thumbnail', 'thumbnail_preview', 'is_active')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def topic_info(self, obj):
        return f"Topic {obj.topic_number}: {obj.title}"
    topic_info.short_description = 'Topic'

    def subject_name(self, obj):
        return obj.chapter.subject.name
    subject_name.short_description = 'Subject'

    def thumbnail_preview(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="150" height="100" style="object-fit: cover; border-radius: 8px;" />',
                obj.thumbnail.url
            )
        return "No thumbnail"
    thumbnail_preview.short_description = 'Thumbnail'

    def notes_count(self, obj):
        return obj.get_notes_count()
    notes_count.short_description = 'Notes'


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ['note_info', 'subject_name', 'chapter_name', 'topic_name', 'page_number', 'image_preview', 'views', 'is_active', 'created_at']
    list_filter = ['topic__chapter__subject', 'topic__chapter', 'topic', 'is_active', 'created_at']
    search_fields = ['title', 'description', 'topic__title', 'topic__chapter__title', 'topic__chapter__subject__name']
    list_editable = ['is_active']
    readonly_fields = ['created_at', 'updated_at', 'views', 'image_preview']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('topic', 'page_number', 'title', 'description')
        }),
        ('Image Upload', {
            'fields': ('image', 'image_preview'),
        }),
        ('Settings & Stats', {
            'fields': ('is_active', 'views')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

    def note_info(self, obj):
        return f"Page {obj.page_number}: {obj.title}"
    note_info.short_description = 'Note'

    def subject_name(self, obj):
        return obj.topic.chapter.subject.name
    subject_name.short_description = 'Subject'

    def chapter_name(self, obj):
        return obj.topic.chapter.title
    chapter_name.short_description = 'Chapter'

    def topic_name(self, obj):
        return obj.topic.title
    topic_name.short_description = 'Topic'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="200" style="border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1);" />',
                obj.image.url
            )
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_editable = ['is_read']
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'created_at')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
    )

    def has_add_permission(self, request):
        # Disable adding contacts from admin (they come from the form)
        return False