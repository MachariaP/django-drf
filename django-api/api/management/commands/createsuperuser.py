# api/management/commands/createsuperuser.py
import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()

class Command(BaseCommand):
    help = "Create a superuser non‑interactively (idempotent)"

    def add_arguments(self, parser):
        parser.add_argument("--username", type=str, default=os.getenv("DJANGO_SUPERUSER_USERNAME"))
        parser.add_argument("--email", type=str, default=os.getenv("DJANGO_SUPERUSER_EMAIL", ""))
        parser.add_argument("--password", type=str, default=os.getenv("DJANGO_SUPERUSER_PASSWORD"))

    def handle(self, *args, **options):
        username = options["username"]
        email = options["email"]
        password = options["password"]

        if not username or not password:
            self.stdout.write(self.style.ERROR("Username and password are required"))
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"Superuser '{username}' already exists – skipping"))
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Superuser '{username}' created"))
