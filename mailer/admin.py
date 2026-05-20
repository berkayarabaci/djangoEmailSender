from django.contrib import admin

from .models import EmailDraft, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "first_name", "last_name", "company", "is_active", "created_at")
    list_filter = ("is_active", "company", "created_at")
    search_fields = ("email", "first_name", "last_name", "company")


@admin.register(EmailDraft)
class EmailDraftAdmin(admin.ModelAdmin):
    list_display = ("subject", "recipient_count", "created_at")
    search_fields = ("subject", "body_text")
    readonly_fields = ("created_at",)
