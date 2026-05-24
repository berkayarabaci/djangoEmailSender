from urllib.parse import urlencode, quote
from urllib.request import Request, urlopen
from urllib.error import URLError

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.html import strip_tags

from .forms import EmailComposeForm, RecipientForm
from .models import EmailDraft, Recipient, WebUser

import html

def build_mailto_url(*, recipients: list[str], subject: str, body_text: str, signature_html: str) -> str:
    signature_text = strip_tags(signature_html).strip()
    full_body = body_text.strip()

    if signature_text:
        full_body = f"{full_body}\n\n{signature_text}"

    bcc_value = ";".join(recipients)

    return (
        "mailto:?"
        f"bcc={quote(bcc_value, safe=';@.')}"
        f"&subject={quote(subject)}"
        f"&body={quote(full_body)}"
    )

def compose_email(request):
    recipients_qs = Recipient.objects.all()
    drafts = EmailDraft.objects.all()

    last_draft = None
    last_draft_id = request.session.pop("last_draft_id", None)

    if last_draft_id:
        last_draft = EmailDraft.objects.filter(id=last_draft_id).first()

    selected_template_id = request.GET.get("template")

    initial_data = {
        "signature_html": "<p>Best regards,<br><strong>Berkay Arabacı</strong><br>Python/Process & Systems</p>"
    }

    if selected_template_id:
        selected_template = get_object_or_404(EmailDraft, pk=selected_template_id)
        initial_data = {
            "template_name": selected_template.template_name,
            "subject": selected_template.subject,
            "body_text": selected_template.body_text,
            "signature_source": selected_template.signature_source,
            "signature_url": selected_template.signature_url,
            "signature_html": selected_template.signature_html,
            "web_user": selected_template.web_user,
            "include_inactive": selected_template.include_inactive,
        }

    if request.method == "POST":
        form = EmailComposeForm(request.POST)

        if form.is_valid():
            include_inactive = form.cleaned_data["include_inactive"]

            selected_recipients_qs = (
                recipients_qs
                if include_inactive
                else recipients_qs.filter(is_active=True)
            )

            recipients = list(selected_recipients_qs.values_list("email", flat=True))

            signature_html = form.cleaned_data["signature_html"]
            signature_source = form.cleaned_data["signature_source"]
            signature_url = form.cleaned_data["signature_url"]
            web_user = form.cleaned_data["web_user"]

            if signature_source == "url":
                if not signature_url:
                    messages.error(request, "Please enter a signature URL.")
                    return redirect("compose_email")

                try:
                    signature_html = load_signature_from_url(signature_url)
                except Exception:
                    messages.error(request, "Could not load signature from the URL.")
                    return redirect("compose_email")

            signature_html = apply_web_user_to_signature(signature_html, web_user)

            if not recipients:
                messages.error(request, "No recipients found. Add recipients first.")
                return redirect("compose_email")

            draft, created = get_or_create_email_template(
                template_name=form.cleaned_data["template_name"],
                subject=form.cleaned_data["subject"],
                body_text=form.cleaned_data["body_text"],
                signature_source=signature_source,
                signature_url=signature_url,
                signature_html=signature_html,
                web_user=web_user,
                include_inactive=include_inactive,
                recipient_count=len(recipients),
            )

            open_outlook_draft(
                recipients=recipients,
                subject=draft.subject,
                body_text=draft.body_text,
                signature_html=draft.signature_html,
            )

            request.session["last_draft_id"] = draft.id

            if created:
                messages.success(
                    request,
                    f"New template saved. Outlook draft opened for {len(recipients)} recipients.",
                )
            else:
                messages.info(
                    request,
                    f"Existing template reused. Outlook draft opened for {len(recipients)} recipients.",
                )

            return redirect("compose_email")
    else:
        form = EmailComposeForm(initial=initial_data)

    return render(
        request,
        "mailer/compose.html",
        {
            "form": form,
            "drafts": drafts,
            "recipient_count": recipients_qs.count(),
            "active_recipient_count": recipients_qs.filter(is_active=True).count(),
            "draft": last_draft,
            "preview_body": last_draft.body_text if last_draft else "",
            "preview_signature_html": last_draft.signature_html if last_draft else "",
        },
    )

def recipient_list(request):
    recipients = Recipient.objects.all().order_by("first_name", "last_name", "email")

    return render(
        request,
        "mailer/recipient_list.html",
        {"recipients": recipients},
    )


def recipient_create(request):
    if request.method == "POST":
        form = RecipientForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("recipient_list")
    else:
        form = RecipientForm()

    return render(
        request,
        "mailer/recipient_form.html",
        {
            "form": form,
            "page_title": "Add Recipient",
            "button_text": "Save Recipient",
        },
    )


def recipient_update(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)

    if request.method == "POST":
        form = RecipientForm(request.POST, instance=recipient)

        if form.is_valid():
            form.save()
            return redirect("recipient_list")
    else:
        form = RecipientForm(instance=recipient)

    return render(
        request,
        "mailer/recipient_form.html",
        {
            "form": form,
            "page_title": "Edit Recipient",
            "button_text": "Update Recipient",
        },
    )


def recipient_delete(request, pk):
    recipient = get_object_or_404(Recipient, pk=pk)

    if request.method == "POST":
        recipient.delete()
        return redirect("recipient_list")

    return render(
        request,
        "mailer/recipient_confirm_delete.html",
        {"recipient": recipient},
    )

def recipient_delete_selected(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_recipients")

        if selected_ids:
            deleted_count, _ = Recipient.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f"{deleted_count} recipient(s) deleted.")
        else:
            messages.warning(request, "No recipients selected.")

    return redirect("recipient_list")

def draft_list(request):
    drafts = EmailDraft.objects.all()

    return render(
        request,
        "mailer/draft_list.html",
        {"drafts": drafts},
    )


def draft_delete(request, pk):
    draft = get_object_or_404(EmailDraft, pk=pk)

    if request.method == "POST":
        draft.delete()
        messages.success(request, "Template deleted.")
        return redirect("draft_list")

    return render(
        request,
        "mailer/draft_confirm_delete.html",
        {"draft": draft},
    )


def draft_delete_selected(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("selected_drafts")

        if selected_ids:
            deleted_count, _ = EmailDraft.objects.filter(id__in=selected_ids).delete()
            messages.success(request, f"{deleted_count} template(s) deleted.")
        else:
            messages.warning(request, "No templates selected.")

    return redirect("draft_list")

def load_signature_from_url(url: str) -> str:
    request = Request(
        url,
        headers={
            "User-Agent": "Outlook Mailer Sender App",
        },
    )

    with urlopen(request, timeout=10) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace")

def open_outlook_draft(*, recipients: list[str], subject: str, body_text: str, signature_html: str) -> None:
    import win32com.client

    outlook = win32com.client.Dispatch("Outlook.Application")
    mail = outlook.CreateItem(0)

    mail.Subject = subject
    mail.BCC = ";".join(recipients)

    body_html = html.escape(body_text).replace("\n", "<br>")

    mail.HTMLBody = f"""
    <html>
        <body>
            <div>{body_html}</div>
            <br>
            {signature_html}
        </body>
    </html>
    """
    mail.Display()

def get_or_create_email_template(
    *,
    template_name: str,
    subject: str,
    body_text: str,
    signature_html: str,
    signature_source: str,
    signature_url: str,
    web_user: WebUser | None,
    include_inactive: bool,
    recipient_count: int,
) -> tuple[EmailDraft, bool]:

    existing_draft = EmailDraft.objects.filter(
        template_name=template_name,
        subject=subject,
        signature_source=signature_source,
        signature_url=signature_url,
        web_user=web_user,
        include_inactive=include_inactive,
    ).first()

    if existing_draft:
        return existing_draft, False

    draft = EmailDraft.objects.create(
        template_name=template_name,
        subject=subject,
        body_text=body_text,
        signature_html=signature_html,
        signature_source=signature_source,
        signature_url=signature_url,
        web_user=web_user,
        include_inactive=include_inactive,
        recipient_count=recipient_count,
    )

    return draft, True

def apply_web_user_to_signature(signature_html: str, web_user: WebUser | None) -> str:
    if not web_user:
        return signature_html

    replacements = {
        "{{DisplayName}}": web_user.display_name,
        "{{JobTitle}}": web_user.job_title,
        "{{Department}}": web_user.department,
        "{{Tel1}}": web_user.tel1,
        "{{Tel2}}": web_user.tel2,
    }

    for placeholder, value in replacements.items():
        signature_html = signature_html.replace(placeholder, value or "")

    return signature_html