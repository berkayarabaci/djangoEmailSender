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


class EmailDraft(models.Model):
    subject = models.CharField(max_length=255)
    body_text = models.TextField()
    signature_html = models.TextField(blank=True)
    recipient_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.subject} ({self.recipient_count} recipients)"
