# Django Outlook Mailer

A portfolio Django project for managing email recipients, reusable email templates, HTML signatures, and opening pre-filled Outlook desktop email drafts.

The app stores recipients, email templates, and signature users in a SQL database. A user can write an email, choose a saved signature user, load an HTML signature from a URL or manual input, preview the message, and open a pre-filled Outlook desktop draft with BCC recipients and HTML signature.

## Features

- Django-based email composer
- Microsoft SQL Server database support
- Recipient management from frontend
  - Add recipients
  - Edit recipients
  - Delete recipients
  - Delete selected recipients
- Email template management
  - Save subject, body, signature settings, and inactive-recipient option
  - Reuse saved templates
  - Delete templates
- Web users table for signature variables
  - `{{DisplayName}}`
  - `{{JobTitle}}`
  - `{{Department}}`
  - `{{Tel1}}`
  - `{{Tel2}}`
- HTML signature support
  - Manual HTML signature input
  - Load signature from URL
- Outlook desktop integration through Windows COM automation
- Opens Outlook draft with:
  - BCC recipients
  - Subject
  - Body
  - HTML signature
- Django admin support
- Portfolio-friendly database table pages

## Important Notes

This project currently uses local Outlook desktop automation through `pywin32`.

That means:

- It works on Windows.
- Microsoft Outlook desktop must be installed.
- The Django app must run on the same computer as Outlook.
- This is not suitable for Linux hosting or cloud deployment in its current version.

For production or cloud usage, Microsoft Graph API is the recommended next step.

## Tech Stack

- Python 3.12
- Django 5.2
- Microsoft SQL Server
- mssql-django
- pyodbc
- pywin32
- HTML/CSS
- Outlook Desktop COM Automation

## Database Tables

Main tables used by the app:

```text
dbo.mailer_recipient
dbo.mailer_emaildraft
dbo.web_users
```
