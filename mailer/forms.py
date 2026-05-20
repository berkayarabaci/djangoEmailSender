from django import forms


class EmailComposeForm(forms.Form):
    subject = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={"placeholder": "Example: Portfolio update"}),
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
