from django import forms

from .models import Subject, Chapter, Topic, Note


class MultiFileInput(forms.ClearableFileInput):
    """File input that allows selecting multiple files."""
    allow_multiple_selected = True


class MultiFileField(forms.FileField):
    """
    A FileField that, when used with MultiFileInput, returns a list of files
    rather than a single file. (Without this, only the last selected file
    would be bound to the field.)
    """
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultiFileInput(attrs={
            'multiple': True,
            'accept': 'image/jpeg,image/png,image/webp',
        }))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result


class BulkUploadForm(forms.Form):
    """
    Studio bulk upload: pick a topic, supply an optional title prefix,
    and select one or more image files.
    """
    topic = forms.ModelChoiceField(
        queryset=Topic.objects.filter(is_active=True)
        .select_related('chapter__subject')
        .order_by('chapter__subject__order', 'chapter__chapter_number', 'topic_number'),
        label='Topic',
        help_text='The topic the new notes will be added to.',
    )
    title_template = forms.CharField(
        max_length=120,
        required=False,
        initial='Note',
        label='Title prefix',
        help_text='Each note will be titled "<prefix> <page>" (e.g. "Note 3").',
    )
    images = MultiFileField(
        label='Note images',
        help_text='Select one or more JPG/PNG/WebP images. They will be added as new pages in order.',
    )


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['name', 'description', 'icon_class', 'order', 'is_active', 'preview_image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['subject', 'title', 'chapter_number', 'description', 'thumbnail', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['chapter', 'title', 'topic_number', 'description', 'thumbnail', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['topic', 'title', 'image', 'page_number', 'description', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
