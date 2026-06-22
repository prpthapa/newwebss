"""
URLs for the private /studio/ section.
"""
from django.urls import path

from . import studio_views

app_name = 'studio'

urlpatterns = [
    path('login/', studio_views.studio_login, name='login'),
    path('logout/', studio_views.studio_logout, name='logout'),
    path('', studio_views.studio_dashboard, name='dashboard'),
    path('upload/', studio_views.studio_upload, name='upload'),
    path('subject/new/', studio_views.studio_new_node, {'kind': 'subject'}, name='new_subject'),
    path('chapter/new/', studio_views.studio_new_node, {'kind': 'chapter'}, name='new_chapter'),
    path('topic/new/', studio_views.studio_new_node, {'kind': 'topic'}, name='new_topic'),
]
