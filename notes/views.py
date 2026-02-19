from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import Subject, Chapter, Topic, Note, ContactMessage
import json
from django.http import HttpResponse


def index(request):
    try:
        subjects = Subject.objects.filter(is_active=True).prefetch_related('chapters')
        context = {
            'subjects': subjects,
        }
        return render(request, 'index.html', context)
    except Exception as e:
        return HttpResponse(f"Error: {str(e)}")
    

def subject_detail(request, slug):
    """
    Subject detail page showing all chapters
    """
    subject = get_object_or_404(Subject, slug=slug, is_active=True)
    chapters = subject.chapters.filter(is_active=True).prefetch_related('topics')
    
    context = {
        'subject': subject,
        'chapters': chapters,
    }
    return render(request, 'subject_detail.html', context)


def chapter_detail(request, subject_slug, chapter_slug):
    """
    Chapter detail page showing all topics
    """
    subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
    chapter = get_object_or_404(
        Chapter, 
        slug=chapter_slug, 
        subject=subject, 
        is_active=True
    )
    topics = chapter.topics.filter(is_active=True).prefetch_related('notes')
    
    context = {
        'subject': subject,
        'chapter': chapter,
        'topics': topics,
    }
    return render(request, 'chapter_detail.html', context)


def topic_detail(request, subject_slug, chapter_slug, topic_slug):
    """
    Topic detail page showing all notes/images
    """
    subject = get_object_or_404(Subject, slug=subject_slug, is_active=True)
    chapter = get_object_or_404(
        Chapter, 
        slug=chapter_slug, 
        subject=subject, 
        is_active=True
    )
    topic = get_object_or_404(
        Topic,
        slug=topic_slug,
        chapter=chapter,
        is_active=True
    )
    notes = topic.notes.filter(is_active=True).order_by('page_number')
    
    context = {
        'subject': subject,
        'chapter': chapter,
        'topic': topic,
        'notes': notes,
    }
    return render(request, 'topic_detail.html', context)


def physics(request):
    """
    Physics subject page
    """
    try:
        subject = Subject.objects.get(slug='physics', is_active=True)
        chapters = subject.chapters.filter(is_active=True).prefetch_related('notes')
        
        context = {
            'subject': subject,
            'chapters': chapters,
        }
        return render(request, 'subject_detail.html', context)
    except Subject.DoesNotExist:
        # Fallback if physics subject doesn't exist
        subjects = Subject.objects.filter(is_active=True)
        return render(request, 'index.html', {'subjects': subjects})


def chemistry(request):
    """
    Chemistry subject page
    """
    try:
        subject = Subject.objects.get(slug='chemistry', is_active=True)
        chapters = subject.chapters.filter(is_active=True).prefetch_related('notes')
        
        context = {
            'subject': subject,
            'chapters': chapters,
        }
        return render(request, 'subject_detail.html', context)
    except Subject.DoesNotExist:
        subjects = Subject.objects.filter(is_active=True)
        return render(request, 'index.html', {'subjects': subjects})


def computer_science(request):
    """
    Computer Science subject page
    """
    try:
        subject = Subject.objects.get(slug='computer-science', is_active=True)
        chapters = subject.chapters.filter(is_active=True).prefetch_related('notes')
        
        context = {
            'subject': subject,
            'chapters': chapters,
        }
        return render(request, 'subject_detail.html', context)
    except Subject.DoesNotExist:
        subjects = Subject.objects.filter(is_active=True)
        return render(request, 'index.html', {'subjects': subjects})


def contact_submit(request):
    """
    Handle contact form submission via AJAX
    """
    if request.method == 'POST':
        try:
            # Get form data
            name = request.POST.get('name', '').strip()
            email = request.POST.get('email', '').strip()
            subject = request.POST.get('subject', '').strip()
            message = request.POST.get('message', '').strip()
            
            # Validate required fields
            if not all([name, email, subject, message]):
                return JsonResponse({
                    'success': False,
                    'message': 'All fields are required.'
                }, status=400)
            
            # Save to database
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            
            # Optional: Send email notification to admin
            try:
                admin_message = f"""
New contact form submission:

Name: {name}
Email: {email}
Subject: {subject}

Message:
{message}
                """
                send_mail(
                    f'New Contact: {subject}',
                    admin_message,
                    settings.EMAIL_HOST_USER if hasattr(settings, 'EMAIL_HOST_USER') else 'noreply@tpradeep.com.np',
                    ['admin@tpradeep.com.np'],  # Change to your admin email
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email send error: {e}")
            
            return JsonResponse({
                'success': True,
                'message': 'Thank you for your message! We will get back to you soon.'
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'An error occurred: {str(e)}'
            }, status=500)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)


def increment_note_view(request, note_id):
    """
    Increment view count for a note (AJAX endpoint)
    """
    if request.method == 'POST':
        try:
            note = get_object_or_404(Note, id=note_id, is_active=True)
            note.increment_views()
            return JsonResponse({
                'success': True,
                'views': note.views
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': str(e)
            }, status=400)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    }, status=405)
