from django import forms
from .models import Recipient, WebUser

class EmailComposeForm(forms.Form):
    template_name = forms.CharField(
        max_length=150,
        required=False,
        label="Template name",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: Monthly update",
            }
        ),
    )

    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Example: Weekly Report"}),
    )

    body_text = forms.CharField(
        label="Body",
        widget=forms.Textarea(
            attrs={
                "rows": 10,
                "placeholder": "Write the main email body here...",
            }
        ),
    )

    SIGNATURE_SOURCE_CHOICES = [
        ("manual", "Use typed signature"),
        ("url", "Load signature from URL"),
    ]

    web_user = forms.ModelChoiceField(
        queryset=WebUser.objects.filter(status=True),
        required=False,
        label="Signature user",
        empty_label="Select signature user",
    )

    signature_source = forms.ChoiceField(
        choices=SIGNATURE_SOURCE_CHOICES,
        initial="manual",
        widget=forms.RadioSelect,
    )

    signature_url = forms.URLField(
        required=False,
        label="Signature URL",
        initial="https://gurdal.com/signature/signature-template.html",
        widget=forms.URLInput(
            attrs={
                "placeholder": "https://example.com/signature.html",
            }
        ),
    )

    signature_html = forms.CharField(
        label="HTML signature",
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 6,
                "placeholder": "<p>Best regards,<br><strong>Your Name</strong></p>",
            }
        ),
        help_text="Used in preview. For mailto compose links, it is converted to plain text.",
    )

    include_inactive = forms.BooleanField(
        required=False,
        label="Include inactive recipients",
    )

class RecipientForm(forms.ModelForm):
    class Meta:
        model = Recipient
        fields = ["first_name", "last_name", "email", "company", "is_active"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "company": forms.TextInput(attrs={"class": "form-control"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }