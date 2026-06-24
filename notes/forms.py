"""
Forms for the public-facing site.

The bulk-upload / studio forms live in `studio_forms.py` to keep this module
focused on user-facing inputs.
"""
from django import forms


class ContactForm(forms.Form):
    """Validated contact form. Used by `notes.views.contact_submit`."""

    name = forms.CharField(
        max_length=100,
        min_length=2,
        strip=True,
        error_messages={
            "required": "Please enter your name.",
            "min_length": "Please enter your full name (at least 2 characters).",
        },
    )
    email = forms.EmailField(
        max_length=254,
        error_messages={
            "required": "Please enter your email address.",
            "invalid": "Please enter a valid email address.",
        },
    )
    subject = forms.CharField(
        max_length=200,
        min_length=3,
        strip=True,
        error_messages={
            "required": "Please enter a subject.",
            "min_length": "Please enter a subject (at least 3 characters).",
        },
    )
    message = forms.CharField(
        widget=forms.Textarea,
        min_length=10,
        max_length=5000,
        strip=True,
        error_messages={
            "required": "Please enter a message.",
            "min_length": "Please enter a message (at least 10 characters).",
            "max_length": "Your message is too long (max 5000 characters).",
        },
    )

    def clean_name(self):
        name = self.cleaned_data.get("name", "")
        # Reject obvious garbage / control chars.
        if any(ord(c) < 32 for c in name):
            raise forms.ValidationError("Name contains invalid characters.")
        return name
