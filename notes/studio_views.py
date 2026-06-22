"""
Studio views: the private /studio/ section.
"""
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .bulk_upload import bulk_create_notes
from .models import Subject, Chapter, Topic, Note
from .studio_auth import (
    SESSION_KEY,
    get_studio_creds,
    studio_login_required,
    do_studio_logout,
)
from .studio_forms import (
    BulkUploadForm,
    SubjectForm,
    ChapterForm,
    TopicForm,
    NoteForm,
)


@require_http_methods(['GET', 'POST'])
def studio_login(request):
    """
    Studio login: check POSTed creds against the configured username/password.
    Sets a session key on success, then redirects to ?next=... (default: dashboard).
    """
    # If already logged in, skip the form.
    if request.session.get(SESSION_KEY):
        return redirect(request.GET.get('next') or 'studio:dashboard')

    error = None
    if request.method == 'POST':
        username = (request.POST.get('username') or '').strip()
        password = request.POST.get('password') or ''
        expected_user, expected_pass = get_studio_creds()
        if username == expected_user and password == expected_pass:
            request.session[SESSION_KEY] = True
            # Cycle the session key after privilege change to prevent fixation.
            request.session.cycle_key()
            next_url = request.POST.get('next') or reverse('studio:dashboard')
            return redirect(next_url)
        error = 'Invalid username or password.'

    return render(request, 'studio/login.html', {
        'next': request.GET.get('next', ''),
        'error': error,
    })


@studio_login_required
def studio_dashboard(request):
    """Studio home: counts, recent uploads, and the subject tree."""
    counts = {
        'subjects': Subject.objects.filter(is_active=True).count(),
        'chapters': Chapter.objects.filter(is_active=True).count(),
        'topics': Topic.objects.filter(is_active=True).count(),
        'notes': Note.objects.filter(is_active=True).count(),
    }
    recent_notes = (
        Note.objects.filter(is_active=True)
        .select_related('topic__chapter__subject')
        .order_by('-created_at')[:10]
    )
    subjects = (
        Subject.objects.filter(is_active=True)
        .prefetch_related('chapters__topics')
        .order_by('order', 'name')
    )
    return render(request, 'studio/dashboard.html', {
        'counts': counts,
        'recent_notes': recent_notes,
        'subjects': subjects,
    })


@studio_login_required
def studio_upload(request):
    """
    Bulk upload: pick a topic, optional title prefix, then one or more images.
    """
    if request.method == 'POST':
        form = BulkUploadForm(request.POST, request.FILES)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            title_prefix = form.cleaned_data.get('title_template') or 'Note'
            files = form.cleaned_data.get('images') or []
            if not files:
                messages.error(request, 'Please choose at least one image.')
            else:
                created = bulk_create_notes(topic, files, title_prefix)
                messages.success(
                    request,
                    f'Successfully uploaded {created} note{"s" if created != 1 else ""} '
                    f'to {topic.chapter.subject.name} / {topic.chapter.title} / {topic.title}.',
                )
                return redirect(f"{reverse('studio:upload')}?topic={topic.id}")
    else:
        initial = {}
        topic_id = request.GET.get('topic')
        if topic_id:
            initial['topic'] = topic_id
        form = BulkUploadForm(initial=initial)

    return render(request, 'studio/upload.html', {'form': form})


@studio_login_required
def studio_new_node(request, kind):
    """
    Generic "new node" view used for subject/chapter/topic.
    ``kind`` must be one of: 'subject', 'chapter', 'topic'.
    """
    form_classes = {
        'subject': SubjectForm,
        'chapter': ChapterForm,
        'topic': TopicForm,
    }
    form_class = form_classes.get(kind)
    if form_class is None:
        messages.error(request, f'Unknown node type: {kind}')
        return redirect('studio:dashboard')

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f'Created {kind}: {obj}.')
            # If we just created a topic, drop the user straight into upload.
            if kind == 'topic':
                return redirect(f"{reverse('studio:upload')}?topic={obj.id}")
            return redirect('studio:dashboard')
    else:
        form = form_class()

    return render(request, 'studio/new_node.html', {
        'form': form,
        'kind': kind,
    })


# Make the logout endpoint importable from urls.py.
studio_logout = do_studio_logout
