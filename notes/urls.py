from django.urls import path, include
from . import views
from .bulk_upload import bulk_upload_notes

urlpatterns = [
    # Home page
    path('', views.index, name='index'),
    
    # Subject specific pages (for backward compatibility with your existing links)
    path('physics/', views.physics, name='physics'),
    path('chemistry/', views.chemistry, name='chemistry'),
    path('computer-science/', views.computer_science, name='computer-science'),
    
    # Dynamic subject page
    path('subject/<slug:slug>/', views.subject_detail, name='subject_detail'),
    
    # Chapter detail page (shows topics)
    path('subject/<slug:subject_slug>/chapter/<slug:chapter_slug>/', 
         views.chapter_detail, 
         name='chapter_detail'),
    
    # Topic detail page (shows notes)
    path('subject/<slug:subject_slug>/chapter/<slug:chapter_slug>/topic/<slug:topic_slug>/', 
         views.topic_detail, 
         name='topic_detail'),
    
    # Bulk upload (admin only)
    path('bulk-upload-notes/', bulk_upload_notes, name='admin_bulk_upload_notes'),

    # Private studio section
    path('studio/', include('notes.studio_urls')),

    # API endpoints
    path('api/contact/', views.contact_submit, name='contact_submit'),
    path('api/note/<int:note_id>/view/', views.increment_note_view, name='increment_note_view'),
]