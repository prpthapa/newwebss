from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from .models import Topic, Note


def bulk_create_notes(topic, files, title_template='Note'):
    """
    Create Note rows for each uploaded file under ``topic``, auto-numbering
    page_number starting from max(page_number)+1 (or 1 if topic has none).

    Returns the number of notes created.
    """
    if not files:
        return 0

    last_note = (
        Note.objects.filter(topic=topic).order_by('-page_number').first()
    )
    start_page = (last_note.page_number + 1) if last_note else 1

    created_count = 0
    for i, file in enumerate(files):
        page_num = start_page + i
        title = f"{title_template} {page_num}"

        Note.objects.create(
            topic=topic,
            title=title,
            image=file,
            page_number=page_num,
            is_active=True,
        )
        created_count += 1

    return created_count


@staff_member_required
def bulk_upload_notes(request):
    """
    Custom view for bulk uploading notes (admin shell).
    """
    topics = Topic.objects.filter(is_active=True).select_related('chapter__subject')

    if request.method == 'POST':
        topic_id = request.POST.get('topic')
        title_template = request.POST.get('title_template', 'Note') or 'Note'
        files = request.FILES.getlist('images')

        if not topic_id or not files:
            messages.error(request, 'Please select a topic and upload at least one image.')
            return redirect('admin_bulk_upload_notes')

        try:
            topic = Topic.objects.get(id=topic_id)
            created_count = bulk_create_notes(topic, files, title_template)
            messages.success(request, f'Successfully uploaded {created_count} notes to {topic.title}!')
            return redirect('admin:notes_note_changelist')
        except Topic.DoesNotExist:
            messages.error(request, 'Selected topic does not exist.')
            return redirect('admin_bulk_upload_notes')
        except Exception as e:
            messages.error(request, f'Error uploading notes: {str(e)}')
            return redirect('admin_bulk_upload_notes')

    context = {
        'topics': topics,
        'title': 'Bulk Upload Notes',
    }
    return render(request, 'admin/bulk_upload_notes.html', context)
