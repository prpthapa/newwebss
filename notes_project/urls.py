from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .health import healthz
from . import views as project_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('studio/', include('notes.studio_urls')),
    path('', include('notes.urls')),

    # Health check (no DB access).
    path('healthz/', healthz, name='healthz'),

    # Legal pages (placeholder content — see plan).
    path('privacy/', project_views.privacy_policy, name='privacy_policy'),
    path('terms/', project_views.terms_of_service, name='terms_of_service'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers — these are looked up by status code when DEBUG=False.
handler404 = 'notes_project.views.page_not_found'
handler500 = 'notes_project.views.server_error'
