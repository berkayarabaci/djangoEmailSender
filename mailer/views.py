from urllib.parse import urlencode

from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse
from django.utils.html import strip_tags

from .forms import EmailComposeForm
from .models import EmailDraft, Recipient


def build_mailto_url(*, recipients: list[str], subject: str, body_text: str, signature_html: str) -> str:
    signature_text = strip_tags(signature_html).strip()
    full_body = body_text.strip()

    if signature_text:
        full_body = f"{full_body}\n\n{signature_text}"

    query = urlencode(
        {
            "bcc": ",".join(recipients),
            "subject": subject,
            "body": full_body,
        }
    )
    return f"mailto:?{query}"


def compose_email(request):
    recipients_qs = Recipient.objects.all()

    if request.method == "POST":
        form = EmailComposeForm(request.POST)

        if form.is_valid():
            include_inactive = form.cleaned_data["include_inactive"]
            selected_recipients_qs = recipients_qs if include_inactive else recipients_qs.filter(is_active=True)
            recipients = list(selected_recipients_qs.values_list("email", flat=True))

            if not recipients:
                messages.error(request, "No recipients found. Add recipients in the admin panel first.")
            else:
                draft = EmailDraft.objects.create(
                    subject=form.cleaned_data["subject"],
                    body_text=form.cleaned_data["body_text"],
                    signature_html=form.cleaned_data["signature_html"],
                    recipient_count=len(recipients),
                )
                mailto_url = build_mailto_url(
                    recipients=recipients,
                    subject=draft.subject,
                    body_text=draft.body_text,
                    signature_html=draft.signature_html,
                )
                messages.success(request, f"Draft saved. Compose link generated for {len(recipients)} recipients.")

                return render(
                    request,
                    "mailer/compose.html",
                    {
                        "form": form,
                        "recipient_count": recipients_qs.count(),
                        "active_recipient_count": recipients_qs.filter(is_active=True).count(),
                        "mailto_url": mailto_url,
                        "draft": draft,
                        "preview_body": draft.body_text,
                        "preview_signature_html": draft.signature_html,
                    },
                )
    else:
        form = EmailComposeForm(
            initial={
                "signature_html": "<p>Best regards,<br><strong>Your Name</strong><br>Python/Django Developer</p>"
            }
        )

    return render(
        request,
        "mailer/compose.html",
        {
            "form": form,
            "recipient_count": recipients_qs.count(),
            "active_recipient_count": recipients_qs.filter(is_active=True).count(),
        },
    )
