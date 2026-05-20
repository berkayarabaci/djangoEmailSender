# Django Outlook Mailer MVP

A small portfolio project built with Django.

The app stores email recipients in a SQL database table, lets a user write an email subject/body/signature, previews the message, and opens the local/default email client through a `mailto:` compose link. SMTP/real sending can be added in version 2.

## Features

- Recipient table in SQLite through Django ORM
- Admin panel for managing recipients
- Email composer form
- Plain-text body input
- HTML signature input and preview
- `mailto:` compose link with recipients in BCC
- Draft history saved to database
- Seed command for demo recipients

## Important note about Outlook and HTML signatures

This MVP uses a `mailto:` link. It opens Outlook only when Outlook is configured as the default mail client on the user's computer. `mailto:` bodies are plain text in practice, so the HTML signature is shown in the web preview and converted to text for the compose window.

In version 2, SMTP or Microsoft Graph can send real HTML emails.

## Tech Stack

- Python 3.11+
- Django 5.2 LTS
- SQLite for local development

## Setup

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run migrations:

```bash
python manage.py migrate
```

Create demo recipients:

```bash
python manage.py seed_recipients
```

Create an admin user:

```bash
python manage.py createsuperuser
```

Run the server:

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

Admin:

```text
http://127.0.0.1:8000/admin/
```

## Version 2 Ideas

- SMTP sending with `django.core.mail.EmailMultiAlternatives`
- Microsoft Graph API integration for Outlook/Microsoft 365
- Email templates
- CSV recipient import
- Recipient groups
- Unsubscribe/status fields
- Send logs and delivery tracking
- Celery background jobs for large batches

## Project Structure

```text
django_outlook_mailer/
├── config/
├── mailer/
│   ├── management/commands/seed_recipients.py
│   ├── templates/mailer/
│   ├── static/mailer/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
├── manage.py
├── requirements.txt
└── README.md
```
