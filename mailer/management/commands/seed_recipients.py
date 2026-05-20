from django.core.management.base import BaseCommand

from mailer.models import Recipient


class Command(BaseCommand):
    help = "Create demo email recipients for local testing."

    def handle(self, *args, **options):
        demo_recipients = [
            {
                "email": "ada@example.com",
                "first_name": "Ada",
                "last_name": "Lovelace",
                "company": "Analytical Engines Ltd",
            },
            {
                "email": "grace@example.com",
                "first_name": "Grace",
                "last_name": "Hopper",
                "company": "Compiler Labs",
            },
            {
                "email": "guido@example.com",
                "first_name": "Guido",
                "last_name": "Rossum",
                "company": "Pythonic Systems",
            },
        ]

        created = 0
        for data in demo_recipients:
            _, was_created = Recipient.objects.get_or_create(email=data["email"], defaults=data)
            created += int(was_created)

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} new recipients."))
