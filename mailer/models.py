from django.db import models
from django.utils import timezone


class Recipient(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=150, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["email"]

    def __str__(self) -> str:
        name = f"{self.first_name} {self.last_name}".strip()
        return f"{name} <{self.email}>" if name else self.email

class WebUser(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100, blank=True)
    job_title = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=150, blank=True)
    tel1 = models.CharField(max_length=50, blank=True)
    tel2 = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "web_users"
        ordering = ["name", "surname"]

    @property
    def display_name(self) -> str:
        return f"{self.name} {self.surname}".strip()

    def __str__(self) -> str:
        return self.display_name


class EmailDraft(models.Model):
    template_name = models.CharField(max_length=150, blank=True)
    subject = models.CharField(max_length=255)
    body_text = models.TextField()

    signature_source = models.CharField(max_length=20, default="manual")
    signature_url = models.URLField(blank=True)
    signature_html = models.TextField(blank=True)

    web_user = models.ForeignKey(
        WebUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    include_inactive = models.BooleanField(default=False)
    recipient_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        if self.template_name:
            return self.template_name
        return f"{self.subject} ({self.recipient_count} recipients)"
