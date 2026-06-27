from django.urls import path, include
from . import views

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
    
    # NOTE: the private /studio/ section is mounted at the project level
    # in `notes_project/urls.py`. Do not include `notes.studio_urls` again
    # here — Django would register the `studio` namespace twice and the
    # second registration would shadow the first, with `reverse()` calls
    # routing to the wrong views.

    # API endpoints
    path('api/contact/', views.contact_submit, name='contact_submit'),
    path('api/note/<int:note_id>/view/', views.increment_note_view, name='increment_note_view'),
]